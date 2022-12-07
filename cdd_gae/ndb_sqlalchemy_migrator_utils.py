"""
Function to migrate from NDB to SQLalchemy.
"""

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


def generate_ndb_to_sqlalchemy_mod(
    name, fields, ndb_mod_to_import, sqlalchemy_mod_to_import
):
    """
    Generate module that contains logic to migrate from NDB to SQLalchemy

    :param name: Module name
    :type name: ```str```

    :param fields: Fields to map in
    :type fields: ```Iterable[str]```

    :param ndb_mod_to_import: NDB module name that the entity will be imported from
    :type ndb_mod_to_import: ```str```

    :param sqlalchemy_mod_to_import: SQLalchemy module name that the entity will be imported from
    :type sqlalchemy_mod_to_import: ```str```

    :return: Module with migration logic from NDB to SQLalchemy
    :rtype: ```Module```
    """
    sql_name = "SQL_{name}".format(name=name)
    ndb_name = "NDB_{name}".format(name=name)
    return Module(
        body=[
            ImportFrom(module="google.cloud", names=[alias(name="ndb")], level=0),
            ImportFrom(
                module="sqlalchemy", names=[alias(name="create_engine")], level=0
            ),
            ImportFrom(
                module="sqlalchemy.orm", names=[alias(name="sessionmaker")], level=0
            ),
            ImportFrom(
                module=ndb_mod_to_import,
                names=[alias(name=name, asname=ndb_name)],
                level=0,
            ),
            ImportFrom(
                module=sqlalchemy_mod_to_import,
                names=[alias(name=name, asname=sql_name)],
                level=0,
            ),
            Assign(
                targets=[Name(id="ndb_client", ctx=Store())],
                value=Call(
                    func=Attribute(
                        value=Name(id="ndb", ctx=Load()), attr="Client", ctx=Load()
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
                        set_value(
                            "postgresql://user:password@localhost:5432/mydatabase"
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
                    keywords=[keyword(arg="bind", value=Name(id="engine", ctx=Load()))],
                ),
                expr=None,
                lineno=None,
                **maybe_type_comment,
            ),
            Assign(
                targets=[Name(id="session", ctx=Store())],
                value=Call(func=Name(id="Session", ctx=Load()), args=[], keywords=[]),
                expr=None,
                lineno=None,
                **maybe_type_comment,
            ),
            Assign(
                targets=[Name(id="query", ctx=Store())],
                value=Call(
                    func=Attribute(
                        value=Name(id=ndb_name, ctx=Load()), attr="query", ctx=Load()
                    ),
                    args=[],
                    keywords=[],
                ),
                expr=None,
                lineno=None,
                **maybe_type_comment,
            ),
            For(
                target=Name(id="ndb_entity", ctx=Store()),
                iter=Call(
                    func=Attribute(
                        value=Name(id="query", ctx=Load()), attr="fetch", ctx=Load()
                    ),
                    args=[],
                    keywords=[],
                ),
                body=[
                    Assign(
                        targets=[Name(id="new_sql_entity", ctx=Store())],
                        value=Call(
                            func=Name(id=sql_name, ctx=Load()),
                            args=[],
                            keywords=list(
                                map(
                                    lambda field: keyword(
                                        arg=field,
                                        value=Attribute(
                                            value=Name(id="ndb_entity", ctx=Load()),
                                            attr=field,
                                            ctx=Load(),
                                        ),
                                    ),
                                    fields,
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
                    func=Attribute(
                        value=Name(id="session", ctx=Load()), attr="commit", ctx=Load()
                    ),
                    args=[],
                    keywords=[],
                )
            ),
        ],
        type_ignores=[],
    )


__all__ = ["generate_ndb_to_sqlalchemy_mod"]
