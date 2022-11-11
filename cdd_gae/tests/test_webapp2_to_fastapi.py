"""
Tests for WebApp2 to FastAPI
"""

from ast import Module, parse
from copy import deepcopy
from functools import partial
from io import StringIO
from os import path
from os.path import extsep
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from cdd.ast_utils import cmp_ast
from cdd.pure_utils import remove_whitespace_comments
from cdd.source_transformer import to_code
from cdd.tests.utils_for_tests import unittest_main

from cdd_gae.tests.mocks.fastapi import (
    hello_fastapi_mod,
    hello_fastapi_str,
    hello_fastapi_with_imports_and_all_mod,
)
from cdd_gae.tests.mocks.webapp2 import hello_webapp2_mod, hello_webapp2_str
from cdd_gae.webapp2_to_fastapi import webapp2_to_fastapi, webapp2_to_fastapi_file


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
            *map(
                partial(str.replace, '"', "'"),
                (
                    remove_whitespace_comments(hello_fastapi_str),
                    to_code(hello_fastapi_mod),
                ),
            )
        )

        self.assertTrue(cmp_ast(hello_webapp2_mod, parse(hello_webapp2_str)))
        self.assertEqual(
            *map(
                remove_whitespace_comments,
                (hello_webapp2_str, to_code(hello_webapp2_mod)),
            )
        )

    def test_empty_webapp2_to_fastapi(self) -> None:
        """Null case"""
        webapp2_mod = Module(body=[], type_ignores=[])
        fastapi_mod = webapp2_to_fastapi(webapp2_mod)
        self.assertTrue(cmp_ast(webapp2_mod, fastapi_mod))

    def test_hello_webapp2_to_hello_fastapi(self) -> None:
        """Test if hello_webapp2 turns into hello_fastapi"""
        fastapi_mod = webapp2_to_fastapi(deepcopy(hello_webapp2_mod))
        hello_fastapi_renamed_func_mod = deepcopy(hello_fastapi_mod)
        hello_fastapi_renamed_func_mod.body[1].name = "HelloWebapp2_get"
        self.assertTrue(cmp_ast(hello_fastapi_renamed_func_mod, fastapi_mod))

    def test_webapp2_to_fastapi_file_dry_run(self) -> None:
        """Test that webapp2_to_fastapi_file works with --dry-run"""
        with patch("sys.stdout", new_callable=StringIO) as sio:
            webapp2_to_fastapi_file("foo", "bar", dry_run=True)
        sio.seek(0)
        self.assertEqual("[webapp2_to_fastapi_file] Dry running\n", sio.read())

    def test_webapp2_to_fastapi_file(self) -> None:
        """
        Tests that `webapp2_to_fastapi_file` creates the right mod
        """
        with TemporaryDirectory() as tmpdir:
            input_file = path.join(tmpdir, "in{extsep}py".format(extsep=extsep))
            output_file = path.join(tmpdir, "out{extsep}py".format(extsep=extsep))
            with open(input_file, "wt") as f:
                f.write(hello_webapp2_str)

            webapp2_to_fastapi_file(input_file=input_file, output_file=output_file)
            with open(output_file, "rt") as f:
                self.assertTrue(
                    cmp_ast(hello_fastapi_with_imports_and_all_mod, parse(f.read()))
                )


unittest_main()
