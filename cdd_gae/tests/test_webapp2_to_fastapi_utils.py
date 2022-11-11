"""
Tests for WebApp2 to FastAPI utils
"""
from _ast import Attribute, Call, Expr, Load, Name
from ast import Module
from copy import deepcopy
from unittest import TestCase

from cdd.ast_utils import cmp_ast, set_value
from cdd.tests.utils_for_tests import unittest_main

from cdd_gae.webapp2_to_fastapi_utils import RewriteResponse


class TestWebApp2toFastApiUtils(TestCase):
    """
    Tests whether ndb classes are parsed correctly
    """

    def test_RewriteResponse_null(self) -> None:
        """
        Tests sanity: whether mocks are internally consistent
        """
        mod = Module(
            body=[
                Expr(
                    value=Call(
                        func=Attribute(
                            value=Attribute(
                                value=Name(id="self", ctx=Load()),
                                attr="response",
                                ctx=Load(),
                            ),
                            attr="overwrite",
                            ctx=Load(),
                        ),
                        args=[set_value("Hello, webapp2!")],
                        keywords=[],
                    )
                ),
            ],
            type_ignores=[],
        )
        new_mod = deepcopy(mod)
        RewriteResponse().visit(new_mod)
        self.assertTrue(cmp_ast(mod, new_mod))


unittest_main()
