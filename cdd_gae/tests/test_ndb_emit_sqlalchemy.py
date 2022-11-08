"""
Tests that NDB parses and then emits SQLalchemy
"""
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from cdd import emit
from cdd.ast_utils import cmp_ast
from cdd.tests.utils_for_tests import unittest_main

from cdd_gae.ndb_parse_emit import ndb_parse_emit_file
from cdd_gae.tests.mocks.ndb import ndb_file_ir, ndb_file_sqlalchemy_cls


class TestNdbEmitSqlAlchemy(TestCase):
    """
    Tests whether SQLalchemy classes are emitted correctly
    """

    def test_emit_sqlalchemy(self) -> None:
        """
        Tests whether emission to SQLalchemy works
        """
        self.assertTrue(
            cmp_ast(
                ndb_file_sqlalchemy_cls,
                emit.sqlalchemy(
                    ndb_file_ir, class_name=ndb_file_ir["name"], emit_repr=False
                ),
            )
        )

    def test_ndb_parse_emit_file_dry_run(self) -> None:
        """Test ndb_parse_emit_file works with --dry-run"""
        with patch("sys.stdout", new_callable=StringIO) as sio:
            ndb_parse_emit_file("foo", "bar", dry_run=True)
        sio.seek(0)
        self.assertEqual("[ndb_parse_emit_file] Dry running\n", sio.read())


unittest_main()
