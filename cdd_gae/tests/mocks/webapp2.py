"""
Mocks for webapp2
"""
from ast import (
    Assign,
    Attribute,
    Call,
    ClassDef,
    Expr,
    FunctionDef,
    List,
    Load,
    Module,
    Name,
    Store,
    Tuple,
    arg,
    arguments,
    keyword,
)

from cdd.ast_utils import maybe_type_comment, set_value

hello_webapp2_str = """
class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')

app = webapp2.WSGIApplication([('/', HelloWebapp2)], debug=True)
"""

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
                        args=[arg(arg="self", annotation=None, **maybe_type_comment)],
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[],
                        vararg=None,
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
                    returns=None,
                    lineno=None,
                    **maybe_type_comment,
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
            expr=None,
            lineno=None,
            **maybe_type_comment,
        ),
    ],
    type_ignores=[],
)

__all__ = ["hello_webapp2_mod", "hello_webapp2_str"]
