"""
Parquet file to an executable insertion `COPY FROM` into a table
"""

from collections import deque
from datetime import datetime
from json import dumps
from operator import methodcaller
from os import environ, path
from sys import stderr

import numpy as np
import psycopg2.sql
from pgcopy import CopyManager
from pyarrow.parquet import ParquetFile
from sqlalchemy import create_engine


def parse_col(col):
    """
    Parse column into something `COPY FROM` can deal with

    :param col: Column
    :type col: ```Any```

    :return: A variant of the input that `COPY FROM` can deal with
    :rtype: ```Any```
    """
    if isinstance(col, np.ndarray):
        return parse_col(col.tolist()) if col.size > 0 else None
    elif isinstance(col, bool):
        return int(col)
    elif isinstance(col, bytes):
        try:
            return parse_col(col.decode("utf8"))
        except UnicodeError:
            print("unable to decode: {!r} ;".format(col), file=stderr)
            raise
    elif isinstance(col, (complex, int)):
        return col
    elif isinstance(col, float):
        return int(col) if col.is_integer() else col
    elif col in (None, "{}", "[]") or not col:
        return None
    elif isinstance(col, str):
        return {"True": 1, "False": 0}.get(col, col)
    elif isinstance(col, (list, tuple, set, frozenset)):
        return list(map(str, map(parse_col, col)))
    elif isinstance(col, dict):
        return dumps(col, separators=(",", ":"))
    elif isinstance(col, datetime):
        return col
    else:
        raise NotImplementedError(type(col))


def psql_insert_copy(table, conn, keys, data_iter):
    """
    Execute SQL statement inserting data

    Parameters
    ----------
    table : pandas.io.sql.SQLTable
    conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys : list of str
        Column names
    data_iter : Iterable that iterates the values to be inserted
    """

    with conn.connection.cursor() as cur:
        table_name = psycopg2.sql.Identifier(
            *(table.schema, table.name) if table.schema else (table.name,)
        ).as_string(cur)

    mgr = CopyManager(
        conn.connection, table.name, keys[1:] if keys and keys[0] == "index" else keys
    )
    mgr.copy(map(lambda line: map(parse_col, line), data_iter))
    conn.connection.commit()


def parquet_to_table(filename, table_name=None, database_uri=None, dry_run=False):
    """
    Parquet file to an executable insertion `COPY FROM` into a table

    :param filename: Path to a Parquet file
    :type filename: ```str```

    :param table_name: Table name to use, else use penultimate underscore surrounding word form filename basename
    :type table_name: ```Optional[str]```

    :param database_uri: Database connection string. Defaults to `RDBMS_URI` in your env vars.
    :type database_uri: ```Optional[str]```

    :param dry_run: Show what would be created; don't actually write to the filesystem
    :type dry_run: ```bool```
    """
    if dry_run:
        print("[parquet_to_table] Dry running")
        return
    parquet_file = ParquetFile(filename)
    engine = create_engine(
        environ["RDBMS_URI"] if database_uri is None else database_uri
    )
    if table_name is None:
        table_name = path.basename(filename).rpartition("_")[0].rpartition("_")[2]
    print("table_name:", table_name, ";")

    deque(
        map(
            lambda df: df.to_sql(
                table_name,
                con=engine,
                if_exists="append",
                method=psql_insert_copy,
                index=False,
            ),
            map(methodcaller("to_pandas"), parquet_file.iter_batches()),
        ),
        maxlen=0,
    )


__all__ = ["parquet_to_table"]
