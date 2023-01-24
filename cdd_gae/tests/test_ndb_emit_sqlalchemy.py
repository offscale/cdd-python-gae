"""
Tests that NDB parses and then emits SQLalchemy
"""

from copy import deepcopy
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

import cdd.emit.sqlalchemy
from cdd.ast_utils import cmp_ast
from cdd.tests.utils_for_tests import unittest_main

from cdd_gae.ndb2sqlalchemy import ndb2sqlalchemy
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
                cdd.emit.sqlalchemy.sqlalchemy(
                    deepcopy(ndb_file_ir),
                    class_name=ndb_file_ir["name"],
                    emit_repr=False,
                ),
                ndb_file_sqlalchemy_cls,
            )
        )

    def test_ndb_parse_emit_file_dry_run(self) -> None:
        """Test ndb_parse_emit_file works with --dry-run"""
        with patch("sys.stdout", new_callable=StringIO) as sio:
            ndb2sqlalchemy("foo", "bar", dry_run=True)
        sio.seek(0)
        self.assertEqual("[ndb_parse_emit_file] Dry running\n", sio.read())


unittest_main()
