"""
Tests for NDB parsing/emitting
"""

from ast import parse
from os import extsep, path
from tempfile import TemporaryDirectory
from unittest import TestCase

from cdd.tests.utils_for_tests import unittest_main
from meta.asttools import cmp_ast

from cdd_gae.ndb_parse_emit import ndb_parse_emit_file
from cdd_gae.tests.mocks.ndb import ndb_file_cls_str, ndb_file_sqlalchemy_output_mod


class TestNdbParseEmit(TestCase):
    """
    Tests whether ndb classes are parsed and emitted correctly
    """

    def test_webapp2_to_fastapi_file(self) -> None:
        """
        Tests that `webapp2_to_fastapi_file` creates the right mod
        """
        with TemporaryDirectory() as tmpdir:
            input_file = path.join(tmpdir, "in{extsep}py".format(extsep=extsep))
            output_file = path.join(tmpdir, "out{extsep}py".format(extsep=extsep))
            with open(input_file, "wt") as f:
                f.write(ndb_file_cls_str)

            ndb_parse_emit_file(input_file=input_file, output_file=output_file)
            with open(output_file, "rt") as f:
                self.assertTrue(
                    cmp_ast(ndb_file_sqlalchemy_output_mod, parse(f.read()))
                )


unittest_main()
