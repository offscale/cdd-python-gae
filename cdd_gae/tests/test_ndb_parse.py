"""
Tests for NDB parsing
"""

from ast import dump, parse
from unittest import TestCase

from cdd.ast_utils import cmp_ast
from cdd.pure_utils import remove_whitespace_comments
from cdd.source_transformer import to_code
from cdd.tests.utils_for_tests import unittest_main

from cdd_gae.parser import ndb
from cdd_gae.tests.mocks.ndb import ndb_file_cls, ndb_file_cls_str, ndb_file_ir


class TestNdbParse(TestCase):
    """
    Tests whether ndb classes are parsed correctly
    """

    def test_sanity(self) -> None:
        """
        Tests sanity: whether mocks are internally consistent
        """
        self.assertEqual(
            cmp_ast(ndb_file_cls, dump(parse(ndb_file_cls_str).body[0])), 0
        )
        self.assertEqual(
            remove_whitespace_comments(ndb_file_cls_str),
            to_code(ndb_file_cls).rstrip("\n"),
        )

    def test_ndb_class_def_to_ir(self) -> None:
        """
        Tests that mock IR matches what `ndb_class_def` creates
        """
        self.assertDictEqual(ndb_file_ir, ndb(ndb_file_cls_str))


unittest_main()
