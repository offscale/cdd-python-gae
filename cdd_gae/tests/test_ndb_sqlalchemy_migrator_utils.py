"""
Tests for ndb sqlalchemy migrator
"""
from unittest import TestCase

from cdd_gae import ndb_sqlalchemy_migrator_utils

import ast
from _ast import Compare, Eq, If, Subscript
from ast import (
    Assign,
    Attribute,
    Call,
    Expr,
    For,
    ImportFrom,
    Load,
    Module,
    Name,
    Store,
    alias,
    keyword,
)
from cdd.ast_utils import maybe_type_comment, set_value


class TestNDBSqlachemyMigratorUtils(TestCase):
    """
    Tests whether SQLAlchemy module is created correctly
    """

    def compare_ast(self, node1, node2):
        if type(node1) != type(node2):
            return False
        elif isinstance(node1, ast.AST):
            for kind, var in vars(node1).items():
                if kind not in ('lineno', 'col_offset', 'ctx'):
                    var2 = vars(node2).get(kind)
                    if not self.compare_ast(var, var2):
                        return False
            return True
        elif isinstance(node1, list):
            if len(node1) != len(node2):
                return False
            for i in range(len(node1)):
                if not self.compare_ast(node1[i], node2[i]):
                    return False
            return True
        else:
            return node1 == node2

    def test_generate_ndb_to_sqlalchemy_mod(self) -> None:
        generated_module = ndb_sqlalchemy_migrator_utils \
            .generate_ndb_to_sqlalchemy_mod("mod_name", ["f1", "f2", "f3"], "ndb_mod", "sqlalchemy_mod")
        exp_module = Module(
            body=[
                ImportFrom(module="os", names=[alias(name="environ", asname="environ")], level=0),
                ImportFrom(module="google.cloud", names=[alias(name="ndb", asname="ndb")], level=0),
                ImportFrom(
                    module="sqlalchemy", names=[alias(name="create_engine", asname="create_engine")], level=0
                ),
                ImportFrom(
                    module="sqlalchemy.orm", names=[alias(name="sessionmaker", asname="sessionmaker")], level=0
                ),
                ImportFrom(
                    module="ndb_mod",
                    names=[alias(name="mod_name", asname="NDB_mod_name")],
                    level=0,
                ),
                ImportFrom(
                    module="sqlalchemy_mod",
                    names=[alias(name="mod_name", asname="SQL_mod_name")],
                    level=0,
                ),
                If(
                    test=Compare(
                        left=Name(id="__name__", ctx=Load()),
                        ops=[Eq()],
                        comparators=[set_value("__main__")],
                    ),
                    body=[
                        Assign(
                            targets=[Name(id="ndb_client", ctx=Store())],
                            value=Call(
                                func=Attribute(
                                    value=Name(id="ndb", ctx=Load()),
                                    attr="Client",
                                    ctx=Load(),
                                ),
                                args=[],
                                keywords=[],
                            ),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment,
                        ),
                        Assign(
                            targets=[Name(id="ndb_context", ctx=Store())],
                            value=Call(
                                func=Attribute(
                                    value=Name(id="ndb_client", ctx=Load()),
                                    attr="context",
                                    ctx=Load(),
                                ),
                                args=[],
                                keywords=[],
                            ),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment,
                        ),
                        Expr(
                            value=Call(
                                func=Attribute(
                                    value=Name(id="ndb_context", ctx=Load()),
                                    attr="set_cache_policy",
                                    ctx=Load(),
                                ),
                                args=[set_value(False)],
                                keywords=[],
                            )
                        ),
                        Assign(
                            targets=[Name(id="engine", ctx=Store())],
                            value=Call(
                                func=Name(id="create_engine", ctx=Load()),
                                args=[
                                    Subscript(
                                        value=Name(id="environ", ctx=Load()),
                                        slice=set_value("RDBMS_URI"),
                                        ctx=Load(),
                                    )
                                ],
                                keywords=[],
                            ),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment,
                        ),
                        Assign(
                            targets=[Name(id="Session", ctx=Store())],
                            value=Call(
                                func=Name(id="sessionmaker", ctx=Load()),
                                args=[],
                                keywords=[
                                    keyword(arg="bind", value=Name(id="engine", ctx=Load()))
                                ],
                            ),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment,
                        ),
                        Expr(
                            value=Call(
                                func=Attribute(
                                    value=Attribute(
                                        value=Name(id="SQL_mod_name", ctx=Load()),
                                        attr="metadata",
                                        ctx=Load(),
                                    ),
                                    attr="create_all",
                                    ctx=Load(),
                                ),
                                args=[Name(id="engine", ctx=Load())],
                                keywords=[],
                            )
                        ),
                        Assign(
                            targets=[Name(id="session", ctx=Store())],
                            value=Call(
                                func=Name(id="Session", ctx=Load()), args=[], keywords=[]
                            ),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment,
                        ),
                        Assign(
                            targets=[Name(id="query", ctx=Store())],
                            value=Call(
                                func=Attribute(
                                    value=Name(id="NDB_mod_name", ctx=Load()),
                                    attr="query",
                                    ctx=Load(),
                                ),
                                args=[],
                                keywords=[],
                            ),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment,
                        ),
                        Assign(
                            targets=[Name(id="entity_no", ctx=Store())],
                            value=set_value(0),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment,
                        ),
                        Assign(
                            targets=[Name(id="batch_size", ctx=Store())],
                            value=set_value(20),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment,
                        ),
                        For(
                            target=Name(id="ndb_entity", ctx=Store()),
                            iter=Call(
                                func=Attribute(
                                    value=Name(id="query", ctx=Load()),
                                    attr="fetch",
                                    ctx=Load(),
                                ),
                                args=[],
                                keywords=[
                                    keyword(arg="offset", value=set_value(0)),
                                    keyword(
                                        arg="batch_size",
                                        value=Name(id="batch_size", ctx=Load()),
                                    ),
                                ],
                            ),
                            body=[
                                Assign(
                                    targets=[Name(id="new_sql_entity", ctx=Store())],
                                    value=Call(
                                        func=Name(id="SQL_mod_name", ctx=Load()),
                                        args=[],
                                        keywords=list(
                                            map(
                                                lambda field: keyword(
                                                    arg=field,
                                                    value=Attribute(
                                                        value=Name(
                                                            id="ndb_entity", ctx=Load()
                                                        ),
                                                        attr=field,
                                                        ctx=Load(),
                                                    ),
                                                ),
                                                ["f1", "f2", "f3"],
                                            )
                                        ),
                                    ),
                                    expr=None,
                                    lineno=None,
                                    **maybe_type_comment,
                                ),
                                Expr(
                                    value=Call(
                                        func=Attribute(
                                            value=Name(id="session", ctx=Load()),
                                            attr="add",
                                            ctx=Load(),
                                        ),
                                        args=[Name(id="new_sql_entity", ctx=Load())],
                                        keywords=[],
                                    )
                                ),
                            ],
                            orelse=[],
                            lineno=None,
                        ),
                        Expr(
                            value=Call(
                                func=Name(id="print", ctx=Load()),
                                args=[
                                    set_value("Committing"),
                                    Name(id="entity_no", ctx=Load()),
                                    set_value("mod_name"),
                                ],
                                keywords=[],
                            )
                        ),
                        Expr(
                            value=Call(
                                func=Attribute(
                                    value=Name(id="session", ctx=Load()),
                                    attr="commit",
                                    ctx=Load(),
                                ),
                                args=[],
                                keywords=[],
                            )
                        ),
                    ],
                    orelse=[],
                ),
            ],
            type_ignores=[],
        )
        self.assertTrue(self.compare_ast(generated_module, exp_module))
