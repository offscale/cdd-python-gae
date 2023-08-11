"""
Tests for Parquet parsing
"""

from collections import OrderedDict
from os import path
from unittest import TestCase

import pyarrow as pa
import pyarrow.parquet as pq
from cdd.tests.utils_for_tests import unittest_main

import cdd_gae.parse.parquet

mocks_dir = path.join(path.dirname(__file__), "mocks")


class TestParseParquet(TestCase):
    """
    Tests whether Parquet files are parsed correctly
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Create parquet file for tests"""
        cls.mock_parquet_file = path.join(mocks_dir, "example.parquet")
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
        pq.write_table(table, cls.mock_parquet_file)

    def test_parquet_to_ir(self) -> None:
        """
        Tests that mock IR matches what `cdd_gae.parse.parquet.parquet` creates
        """
        self.assertDictEqual(
            cdd_gae.parse.parquet.parquet(self.mock_parquet_file),
            {
                "name": "example.parquet",
                "params": OrderedDict(
                    (
                        (
                            "n_legs",
                            {"typ": "int", "x_typ": {"sql": {"type": "BigInteger"}}},
                        ),
                        ("animal", {"typ": "str"}),
                    )
                ),
                "returns": None,
            },
        )


unittest_main()
