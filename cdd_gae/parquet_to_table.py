"""
Parquet file to an executable insertion `COPY FROM` into a table
"""

from collections import deque
from datetime import datetime
from functools import partial
from json import dumps, loads
from operator import methodcaller
from os import environ, path

import numpy as np
import psycopg2.sql
from cdd.shared.pure_utils import identity
from pgcopy import CopyManager
from pyarrow.parquet import ParquetFile
from sqlalchemy import create_engine


def postgres_csvify(col):
    return (
        str(col)
        .replace("[", "{")
        .replace("]", "}")
        .replace("None", "null")
        .replace("'", '"')
        .replace('""', '"')
        .replace(': ",', ': "",')
    )


def parse_col(col):
    """
    Parse column into something `COPY FROM` can deal with on a CSV read

    :param col: Column
    :type col: ```Any```

    :return: A variant of the input that `COPY FROM` can deal with on a CSV read
    :rtype: ```Any```
    """
    if isinstance(col, np.ndarray):
        return parse_col(col.tolist()) if col.size > 0 else "null"
    elif isinstance(col, bool):
        return int(col)
    elif isinstance(col, bytes):
        try:
            return parse_col(col.decode("utf8"))
        except UnicodeError:
            print("unable to decode: {!r} ;".format(col))
            raise
    elif isinstance(col, (complex, int)):
        return col
    elif isinstance(col, float):
        return int(col) if col.is_integer() else col
    elif col in (None, "{}", "[]") or not col:
        return "null"
    elif isinstance(col, str):
        return {"True": 1, "False": 0}.get(col, col)
    elif isinstance(col, (list, tuple, set, frozenset)):
        return "{{{0}{1}}}".format(
            ",".join(map(partial(dumps, separators=(",", ":")), map(parse_col, col))),
            "," if len(col) == 1 else "",
        )
    elif isinstance(col, dict):
        return dumps(col, separators=(",", ":"))
    elif isinstance(col, datetime):
        return col.isoformat()
    else:
        raise NotImplementedError(type(col))


# {"\\"first item\\"","\\"second item\\"",
#  "\\"third item with \\\\\\"quotes\\\\\\" inside\\"","\\"fourth with a \\\\\\\\ backslash\\""}


def maybe_quote_and_escape(s, ch='"'):
    if isinstance(s, str) and s.startswith("{") and s.endswith("}"):
        return "{ch}{}{ch}".format(s.replace('"', '\\"'), ch=ch)
    return s


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


def csv_to_postgres_text(lines):
    return "\n".join(map(csv_to_postgres_line, lines.split("\n")))


def csv_to_postgres_line(line):
    columns = line.split(
        "\t"
    )  # TODO: Handle escaped strings that contain the tab character
    return "\t".join(map(csv_col_to_postgres_col, columns))


def csv_col_to_postgres_col(col):
    is_array = col.startswith("[") and col.endswith("]")
    if is_array or col.startswith("{") and col.endswith("}"):
        col_parsed = loads(col.replace("'", '"'))
        if is_array:
            col = "{{{0}}}".format(
                ",".join(
                    map(
                        lambda a: identity(a)
                        if not col_parsed
                        or isinstance(col_parsed[0], (str, bytes, complex, float, int))
                        else repr(a).replace('"', '\\"'),
                        map(partial(dumps, separators=(",", ":")), col_parsed),
                    )
                )
            )
        else:
            col = dumps(
                col_parsed, separators=(",", ":")
            )  # .replace("[", "{").replace("]", "}")

    return col.replace("'", '"')


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
