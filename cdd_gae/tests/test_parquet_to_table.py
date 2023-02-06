"""
Tests for Parquet to Table
"""
from unittest import TestCase
from cdd_gae import parquet_to_table
import datetime
import pyarrow.parquet as pq
import psycopg2
import pandas as pd
import pyarrow as pa
import os


class TestParquetToTable(TestCase):
    """
    Tests whether Parquet to table methods work correctly
    """
    def test_parse_col(self) -> None:
        """
        Test that `parse_col` produces something `COPY FROM` can deal with on a CSV read
        """
        self.assertEqual(parquet_to_table.parse_col("String"), "String")
        self.assertEqual(parquet_to_table.parse_col(1), 1)
        self.assertEqual(parquet_to_table.parse_col(complex(1, 1)), complex(1, 1))
        self.assertEqual(parquet_to_table.parse_col(bytes("message", 'utf-8')), bytes("message", 'utf-8'))
        self.assertEqual(parquet_to_table.parse_col(set([1, 2, 3])), set([1, 2, 3]))
        self.assertEqual(parquet_to_table.parse_col(frozenset([1, 2, 3])), frozenset([1, 2, 3]))
        self.assertEqual(parquet_to_table.parse_col(None), None)
        self.assertEqual(parquet_to_table.parse_col(5.0), 5)
        self.assertEqual(parquet_to_table.parse_col(5.1), 5.1)
        self.assertEqual(parquet_to_table.parse_col([]), "{}")
        self.assertEqual(parquet_to_table.parse_col(()), "{}")
        self.assertEqual(parquet_to_table.parse_col([1, 2]), [1, 2])
        self.assertEqual(parquet_to_table.parse_col({"foo": "bar"}), """{"foo": "bar"}""")
        self.assertEqual(parquet_to_table.parse_col(datetime.datetime(2020, 5, 17)),
                         datetime.datetime(2020, 5, 17).isoformat())
        self.assertRaises(NotImplementedError, parquet_to_table.parse_col, (lambda x: x))

    # Test only passes locally so it is commented out for now

    # def test_parquet_to_table(self) -> None:
    #     """
    #     Test that sql data is properly inserted from parquet file
    #     """
    #     df = pd.DataFrame({'f1': ["1"],
    #                        'f2': ["2"],
    #                        'f3': ["3"]})
    #     table = pa.Table.from_pandas(df)
    #     pq.write_table(table, 'example.parquet')
    #     parquet_to_table.parquet_to_table('example.parquet', 'fields', "postgresql://postgres:newpasssharonb123@localhost:5432/postgres")
    #
    #     try:
    #         connection = psycopg2.connect(user="postgres",
    #                                       password="newpasssharonb123",
    #                                       host="127.0.0.1",
    #                                       port="5432",
    #                                       database="postgres")
    #         cursor = connection.cursor()
    #         cursor.execute("select * from fields")
    #         records = cursor.fetchall()
    #
    #         self.assertEqual(records[0][0], "1")
    #         self.assertEqual(records[0][1], "2")
    #         self.assertEqual(records[0][2], "3")
    #
    #         cursor.execute("TRUNCATE fields")  # deleting all rows
    #         os.remove("example.parquet")
    #     except (Exception, psycopg2.Error) as error:
    #         print("Error while fetching data from PostgreSQL", error)
    #     finally:
    #         if connection:
    #             cursor.close()
    #             connection.close()
