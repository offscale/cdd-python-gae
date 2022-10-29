"""
Mocks for webapp2
"""
from ast import (
    List,
    Tuple,
    keyword,
    Store,
    Name,
    Assign,
    Module,
    ClassDef,
    Load,
    Attribute,
    FunctionDef,
    arguments,
    arg,
    Expr,
    Call,
)

from cdd.ast_utils import set_value

hello_webapp2_mod = Module(
    body=[
        ClassDef(
            name="HelloWebapp2",
            bases=[
                Attribute(
                    value=Name(id="webapp2", ctx=Load()),
                    attr="RequestHandler",
                    ctx=Load(),
                )
            ],
            keywords=[],
            body=[
                FunctionDef(
                    name="get",
                    args=arguments(
                        posonlyargs=[],
                        args=[arg(arg="self")],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=[
                        Expr(
                            value=Call(
                                func=Attribute(
                                    value=Attribute(
                                        value=Name(id="self", ctx=Load()),
                                        attr="response",
                                        ctx=Load(),
                                    ),
                                    attr="write",
                                    ctx=Load(),
                                ),
                                args=[set_value("Hello, webapp2!")],
                                keywords=[],
                            )
                        )
                    ],
                    decorator_list=[],
                )
            ],
            decorator_list=[],
        ),
        Assign(
            targets=[Name(id="app", ctx=Store())],
            value=Call(
                func=Attribute(
                    value=Name(id="webapp2", ctx=Load()),
                    attr="WSGIApplication",
                    ctx=Load(),
                ),
                args=[
                    List(
                        elts=[
                            Tuple(
                                elts=[
                                    set_value("/"),
                                    Name(id="HelloWebapp2", ctx=Load()),
                                ],
                                ctx=Load(),
                            )
                        ],
                        ctx=Load(),
                    )
                ],
                keywords=[keyword(arg="debug", value=set_value(True))],
            ),
        ),
    ],
    type_ignores=[],
)

__all__ = ["hello_webapp2_mod"]
