"""
Mocks for Sqlalchemy
"""
from ast import Assign, Attribute, Call, Expr, For, ImportFrom, Load, Module, Name, Store, alias, keyword, Compare, Eq, If, Subscript
from cdd.shared.ast_utils import maybe_type_comment, set_value

sqlalchemy_class_file_str = """
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
# declarative base class
Base = declarative_base()
# an example mapping using the base
class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
"""

ndb_to_sqlalchemy_migration_mod = Module(
        body=[
            ImportFrom(
                module="os", names=[alias(name="environ", asname="environ")], level=0
            ),
            ImportFrom(
                module="google.cloud", names=[alias(name="ndb", asname="ndb")], level=0
            ),
            ImportFrom(
                module="sqlalchemy",
                names=[alias(name="create_engine", asname="create_engine")],
                level=0,
            ),
            ImportFrom(
                module="sqlalchemy.orm",
                names=[alias(name="sessionmaker", asname="sessionmaker")],
                level=0,
            ),
            ImportFrom(
                module="example_ndb",
                names=[alias(name="Person", asname="NDB_Person")],
                level=0,
            ),
            ImportFrom(
                module="example_sql",
                names=[alias(name="Person", asname="SQL_Person")],
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
                                    value=Name(id="SQL_Person", ctx=Load()),
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
                                value=Name(id="NDB_Person", ctx=Load()),
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
                                    func=Name(id="SQL_Person", ctx=Load()),
                                    args=[],
                                    keywords=[keyword(
                                                arg="name",
                                                value=Attribute(
                                                    value=Name(
                                                        id="ndb_entity", ctx=Load()
                                                    ),
                                                    attr="name",
                                                    ctx=Load(),
                                                ),
                                            ), keyword(
                                                arg="fullname",
                                                value=Attribute(
                                                    value=Name(
                                                        id="ndb_entity", ctx=Load()
                                                    ),
                                                    attr="fullname",
                                                    ctx=Load(),
                                                ),
                                            ), keyword(
                                                arg="nickname",
                                                value=Attribute(
                                                    value=Name(
                                                        id="ndb_entity", ctx=Load()
                                                    ),
                                                    attr="nickname",
                                                    ctx=Load(),
                                                ),
                                            )],
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
                                set_value("Person"),
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

__all__ = ["sqlalchemy_class_file_str", "ndb_to_sqlalchemy_migration_mod"]
