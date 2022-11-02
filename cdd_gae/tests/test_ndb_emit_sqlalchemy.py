"""
Tests that NDB parses and then emits SQLalchemy
"""
from unittest import TestCase

from cdd import emit
from cdd.ast_utils import cmp_ast
from cdd.tests.utils_for_tests import unittest_main

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


unittest_main()
