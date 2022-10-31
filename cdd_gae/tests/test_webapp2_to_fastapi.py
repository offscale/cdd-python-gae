"""
Tests for WebApp2 to FastAPI
"""

from ast import parse, dump
from unittest import TestCase

from cdd.ast_utils import cmp_ast
from cdd.pure_utils import remove_whitespace_comments, pp
from cdd.source_transformer import to_code
from cdd.tests.utils_for_tests import unittest_main

from cdd_gae.tests.mocks.fastapi import hello_fastapi_str, hello_fastapi_mod
from cdd_gae.tests.mocks.webapp2 import hello_webapp2_mod, hello_webapp2_str


class TestWebApp2toFastApi(TestCase):
    """
    Tests whether ndb classes are parsed correctly
    """

    def test_sanity(self) -> None:
        """
        Tests sanity: whether mocks are internally consistent
        """
        self.assertTrue(cmp_ast(hello_fastapi_mod, parse(hello_fastapi_str)))
        self.assertEqual(
            remove_whitespace_comments(hello_fastapi_str), to_code(hello_fastapi_mod)
        )

        self.assertTrue(cmp_ast(hello_webapp2_mod, parse(hello_webapp2_str)))
        self.assertEqual(
            remove_whitespace_comments(hello_webapp2_str), to_code(hello_webapp2_mod)
        )

    maxDiff = None


unittest_main()
