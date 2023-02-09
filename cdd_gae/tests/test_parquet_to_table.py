"""
Tests for Parquet to Table
"""

import datetime
from unittest import TestCase

from cdd.tests.utils_for_tests import unittest_main

from cdd_gae import parquet_to_table


class TestParquetToTable(TestCase):
    """
    Tests whether Parquet to table methods work correctly
    """

    def test_parse_col(self) -> None:
        """
        Tess that `parse_col` produces something `COPY FROM` can deal with on a CSV read
        """
        self.assertEqual(parquet_to_table.parse_col("String"), "String")
        self.assertEqual(parquet_to_table.parse_col(1), 1)
        self.assertEqual(parquet_to_table.parse_col(complex(1, 1)), complex(1, 1))
        self.assertEqual(
            parquet_to_table.parse_col(bytes("message", "utf-8")),
            bytes("message", "utf-8"),
        )
        self.assertEqual(parquet_to_table.parse_col(set([1, 2, 3])), set([1, 2, 3]))
        self.assertEqual(
            parquet_to_table.parse_col(frozenset([1, 2, 3])), frozenset([1, 2, 3])
        )
        self.assertEqual(parquet_to_table.parse_col(None), None)
        self.assertEqual(parquet_to_table.parse_col(5.0), 5)
        self.assertEqual(parquet_to_table.parse_col(5.1), 5.1)
        self.assertEqual(parquet_to_table.parse_col([]), "{}")
        self.assertEqual(parquet_to_table.parse_col(()), "{}")
        self.assertEqual(
            parquet_to_table.parse_col({"foo": "bar"}), """{"foo": "bar"}"""
        )
        self.assertEqual(
            parquet_to_table.parse_col(datetime.datetime(2020, 5, 17)),
            datetime.datetime(2020, 5, 17).isoformat(),
        )


unittest_main()
