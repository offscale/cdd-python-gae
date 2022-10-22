"""
Tests for docstring parsing
"""

from ast import parse, unparse, dump
from os import path
from unittest import TestCase

from cdd.ast_utils import cmp_ast
from cdd.pure_utils import remove_whitespace_comments
from cdd.source_transformer import to_code
from cdd.tests.utils_for_tests import unittest_main

from cdd_gae.tests.mocks.ndb import ndb_file_cls, ndb_file_cls_str


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
            remove_whitespace_comments(ndb_file_cls_str), to_code(ndb_file_cls)
        )


unittest_main()
