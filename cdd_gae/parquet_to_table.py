"""
Parquet file to an executable insertion `COPY FROM` into a table
"""

import csv
from collections import deque
from datetime import datetime
from io import StringIO
from json import dumps
from operator import methodcaller
from os import environ, path

import numpy as np
from pyarrow.parquet import ParquetFile
from sqlalchemy import create_engine


def parse_col(col):
    """
    Parse column into something SQLalchemy can deal with

    :param col: Column
    :type col: ```Any```

    :return: A variant of the input that SQLalchemy can deal with
    :rtype: ```Any```
    """
    if isinstance(col, (str, complex, int, bytes, set, frozenset, type(None))):
        return col
    elif isinstance(col, float):
        return int(col) if col.is_integer() else col
    elif isinstance(col, (list, tuple, np.ndarray)):
        if len(col) == 0:
            # return 'array[]::varchar[]'
            # return dumps('NULL')
            return "{}"
        return col
    elif isinstance(col, dict):
        return dumps(col)
    elif isinstance(col, datetime):
        return col.isoformat()
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
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        data_iter = map(lambda record: tuple(map(parse_col, record[1:])), data_iter)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ", ".join(map('"{}"'.format, keys[1:]))
        if table.schema:
            table_name = '{}."{}"'.format(table.schema, table.name)
        else:
            table_name = table.name

        print("s_buf:")
        print(s_buf.read())
        s_buf.seek(0)
        sql = 'COPY "{}" ({}) FROM STDIN WITH CSV'.format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


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

    deque(
        map(
            lambda df: df.to_sql(
                table_name, con=engine, if_exists="append", method=psql_insert_copy
            ),
            map(methodcaller("to_pandas"), parquet_file.iter_batches(batch_size=1)),
        ),
        maxlen=0,
    )


__all__ = ["parquet_to_table"]
