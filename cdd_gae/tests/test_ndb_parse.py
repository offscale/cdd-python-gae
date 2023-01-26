"""
Tests for NDB parsing
"""

from ast import parse
from collections import OrderedDict
from unittest import TestCase

from cdd.ast_utils import cmp_ast, get_value
from cdd.pure_utils import remove_whitespace_comments
from cdd.source_transformer import to_code
from cdd.tests.utils_for_tests import unittest_main

from cdd_gae.parse.ndb import ndb
from cdd_gae.tests.mocks.ndb import ndb_file_cls, ndb_file_cls_str, ndb_file_ir


class TestNdbParse(TestCase):
    """
    Tests whether ndb classes are parsed correctly
    """

    def test_sanity(self) -> None:
        """
        Tests sanity: whether mocks are internally consistent
        """
        self.assertTrue(cmp_ast(ndb_file_cls, parse(ndb_file_cls_str).body[0]))
        self.assertEqual(
            remove_whitespace_comments(ndb_file_cls_str),
            to_code(ndb_file_cls).rstrip("\n"),
        )

    def test_ndb_class_def_to_ir(self) -> None:
        """
        Tests that mock IR matches what `ndb_class_def` creates
        """
        ir = ndb(ndb_file_cls_str, "File")

        def dict_unroll(d):
            """
            Unroll a dictionary (i.e., flatten)

            :type d: ```dict```

            :rtype: ```dict```
            """
            return (
                {k: dict_unroll(get_value(v)) for k, v in d.items()}
                if isinstance(d, dict)
                else d
            )

        ir["params"] = OrderedDict(
            (
                (
                    name,
                    {key: dict_unroll(val) for key, val in param.items()},
                )
                for name, param in ir["params"].items()
            )
        )
        ir["params"]["updated"]["x_typ"]["sql"]["constraints"][
            "onupdate"
        ] = ndb_file_ir["params"]["updated"]["x_typ"]["sql"]["constraints"]["onupdate"]

        self.assertDictEqual(ndb_file_ir, ir)

    maxDiff = None


unittest_main()
