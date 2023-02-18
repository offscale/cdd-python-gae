"""
Tests for Parquet to Table
"""

import unittest
from datetime import datetime
from os import environ, path
from tempfile import TemporaryDirectory
from unittest import TestCase

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sqlalchemy
from cdd.tests.utils_for_tests import unittest_main
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
)

from cdd_gae.parquet_to_table import parquet_to_table

no_conflict_in_table_name_table_name = "no_conflict_in_table_name"
metadata = MetaData()
no_conflict_in_table_name_tbl = Table(
    no_conflict_in_table_name_table_name,
    metadata,
    Column("timestamp_col", TIMESTAMP(timezone=True)),
    Column("json_col", JSON),
    Column("array_str_col", ARRAY(String)),
    Column("array_bigint_col", ARRAY(BigInteger)),
    Column("array_json_col", ARRAY(JSON)),
    Column("id", Integer, primary_key=True, server_default=Identity()),
)


class TestParquetToTable(TestCase):
    """
    Tests whether `COPY FROM` is correctly generated from `parquet_to_table`
    """

    @unittest.skipIf("RDMBS_URI" not in environ)
    def test_parquet_to_table(self) -> None:
        """
        Tests complex rows are inserted into table using parquet_to_table
        """
        engine = create_engine(environ["RDBMS_URI"])
        try:
            metadata.create_all(engine)
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
                parquet_to_table(
                    parquet_filepath, table_name=no_conflict_in_table_name_table_name
                )
        finally:
            if sqlalchemy.inspect(engine).has_table(
                no_conflict_in_table_name_table_name
            ):
                metadata.drop_all(tables=[no_conflict_in_table_name_tbl], bind=engine)


unittest_main()
