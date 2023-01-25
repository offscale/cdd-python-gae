"""
Tests for Parquet parsing
"""
from collections import OrderedDict
from unittest import TestCase

import pyarrow as pa
from cdd.tests.utils_for_tests import unittest_main

import cdd_gae.parse.parquet_utils


class TestParseParquetUtils(TestCase):
    """
    Tests whether Parquet columns are parsed correctly
    """

    def test_parquet_type_to_param(self) -> None:
        """
        Tests that `parquet_type_to_param` produces a `param` that can be merged into python_cdd IR.
        """
        self.assertRaises(
            NotImplementedError,
            cdd_gae.parse.parquet_utils.parquet_type_to_param,
            pa.Field,
        )
        table = pa.table(
            {
                "n_legs": [2, 2, 4, 4, 5, 100],
                "animal": [
                    "Flamingo",
                    "Parrot",
                    "Dog",
                    "Horse",
                    "Brittle stars",
                    "Centipede",
                ],
            }
        )
        self.assertDictEqual(
            cdd_gae.parse.parquet_utils.parquet_type_to_param(table.column(0)),
            {"typ": "int64"},
        )
        self.assertDictEqual(
            cdd_gae.parse.parquet_utils.parquet_type_to_param(
                pa.field("id", pa.string())
            ),
            {"typ": "string"},
        )
        self.assertDictEqual(
            cdd_gae.parse.parquet_utils.parquet_type_to_param(
                # pa.field("list_field", pa.list_(pa.DataType("string")))
                pa.field(
                    "some_structure",
                    pa.struct([pa.field("value", pa.int64(), nullable=False)]),
                )
            ),
            {
                "ir": {
                    "name": "some_structure",
                    "params": OrderedDict(
                        (("some_structure.value", {"typ": "int64"}),)
                    ),
                    "returns": None,
                },
                "typ": "dict",
            },
        )
        self.assertDictEqual(
            cdd_gae.parse.parquet_utils.parquet_type_to_param(
                pa.field("value", pa.int64(), nullable=False)
            ),
            {"typ": "int64"},
        )
        self.assertDictEqual(
            cdd_gae.parse.parquet_utils.parquet_type_to_param(
                pa.field("list_ints", pa.list_(pa.int64()), nullable=False)
            ),
            {"typ": "List[int64]"},
        )
        self.assertDictEqual(
            cdd_gae.parse.parquet_utils.parquet_type_to_param(
                pa.field(
                    "the_time", pa.timestamp("s", tz="America/New_York"), nullable=False
                )
            ),
            {"typ": "timestamp[s, tz=America/New_York]"},
        )


unittest_main()
