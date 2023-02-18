"""
Tests for Parquet to Table
"""

import inspect
import unittest
from copy import deepcopy
from datetime import datetime
from itertools import repeat
from os import environ, path
from tempfile import TemporaryDirectory
from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sqlalchemy
from cdd.tests.utils_for_tests import unittest_main
from psycopg2.extensions import AsIs, register_adapter
from sqlalchemy import (
    ARRAY,
    JSON,
    TIMESTAMP,
    BigInteger,
    Column,
    Identity,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    orm,
)
from sqlalchemy.orm import Query, Session

from cdd_gae.parquet_to_table import parquet_to_table

metadata = MetaData()


def construct_table(table_name):
    return Table(
        table_name,
        metadata,
        Column("timestamp_col", TIMESTAMP(timezone=True)),
        Column("json_col", JSON),
        Column("array_str_col", ARRAY(String)),
        Column("array_bigint_col", ARRAY(BigInteger)),
        Column("array_json_col", ARRAY(JSON)),
        Column("id", Integer, primary_key=True, server_default=Identity()),
    )


def with_own_table(f):
    """
    Create table just for this test. Drop table after.
    """

    def inner(*args, **kwargs):
        engine = create_engine(environ["RDBMS_URI"])
        table = construct_table(f.__name__)
        metadata.create_all(engine)
        try:
            return f(*args, **kwargs)
        finally:
            if sqlalchemy.inspect(engine).has_table(f.__name__):
                metadata.drop_all(tables=[table], bind=engine)

    return inner


def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)


def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)


register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)


class TestParquetToTable(TestCase):
    """
    Tests whether `COPY FROM` is correctly generated from `parquet_to_table`
    """

    @unittest.skipUnless(
        "RDBMS_URI" in environ, "RDMBS_URI env var must be set to for this test to run"
    )
    def test_sqlalchemy_csv(self) -> None:
        """Reverse-engineer SQLalchemy's handling of complex types for cdd_gae's implementation"""

        table_name = inspect.stack()[0].function

        class Tbl:
            """"""

        engine = create_engine(environ["RDBMS_URI"])
        mapper_registry = orm.registry()

        table = construct_table(table_name)
        mapper_registry.map_imperatively(Tbl, table)

        metadata.create_all(engine)

        try:
            with Session(engine) as session:
                self.assertEqual(Query([Tbl], session=session).count(), 0)
                session.add_all(
                    map(
                        deepcopy,
                        repeat(
                            Tbl(
                                timestamp_col="2023-02-18 17:14:43.592777+00:00",  # datetime.now(),
                                json_col={"can": "haz"},
                                array_str_col=["Flamingo", "Centipede"],
                                array_bigint_col=np.arange(6, dtype=np.int64),
                                array_json_col=[{"foo": "bar"}, {"can": "haz"}],
                            ),
                            3,
                        ),
                    )
                )
                session.commit()
                self.assertEqual(Query([Tbl], session=session).count(), 3)
                results = pd.read_sql_query(
                    "select * from {}".format(table_name), engine
                ).to_csv(index=False, sep="\t")
                self.assertEqual(
                    results,
                    "\n".join(
                        (
                            "timestamp_col	json_col	array_str_col	array_bigint_col	array_json_col	id",
                            "2023-02-18 17:14:43.592777+00:00	{'can': 'haz'}	['Flamingo', 'Centipede']	[0, 1, 2, 3, 4, 5]	[{'foo': 'bar'}, {'can': 'haz'}]	1",
                            "2023-02-18 17:14:43.592777+00:00	{'can': 'haz'}	['Flamingo', 'Centipede']	[0, 1, 2, 3, 4, 5]	[{'foo': 'bar'}, {'can': 'haz'}]	2",
                            "2023-02-18 17:14:43.592777+00:00	{'can': 'haz'}	['Flamingo', 'Centipede']	[0, 1, 2, 3, 4, 5]	[{'foo': 'bar'}, {'can': 'haz'}]	3\n",
                        )
                    )
                )
        finally:
            if sqlalchemy.inspect(engine).has_table(table_name):
                metadata.drop_all(tables=[table], bind=engine)

    @unittest.skipUnless(
        "RDBMS_URI" in environ, "RDMBS_URI env var must be set to for this test to run"
    )
    @with_own_table
    def test_parquet_to_table(self) -> None:
        """
        Tests complex rows are inserted into table using parquet_to_table
        """
        row = pa.table(
            pd.DataFrame(
                {
                    "timestamp_col": datetime.now().isoformat(),
                    "json_col": {"can": "haz"},
                    "array_str_col": ["Flamingo", "Centipede"],
                    "array_bigint_col": np.arange(6, dtype=np.int64),
                    "array_json_col": [{"foo": "bar"}, {"can": "haz"}],
                }
            )
        )
        with TemporaryDirectory() as tempdir:
            parquet_filepath = path.join(tempdir, "foo.parquet")
            pq.write_table(row, parquet_filepath)
            parquet_to_table(parquet_filepath, table_name=inspect.stack()[0].function)


unittest_main()
