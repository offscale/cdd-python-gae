"""
FastAPI mocks that match those in webapp2.py
"""

from ast import (
    Assign,
    Attribute,
    Call,
    FunctionDef,
    Load,
    Module,
    Name,
    Return,
    Store,
    arguments,
)

from cdd.ast_utils import maybe_type_comment, set_value

hello_fastapi_str = """
app = FastAPI()


@app.get("/")
def read_root():
    return "Hello, webapp2!"
"""

hello_fastapi_mod = Module(
    body=[
        Assign(
            targets=[Name(id="app", ctx=Store())],
            value=Call(func=Name(id="FastAPI", ctx=Load()), args=[], keywords=[]),
            expr=None,
            lineno=None,
            **maybe_type_comment
        ),
        FunctionDef(
            name="read_root",
            args=arguments(
                posonlyargs=[],
                args=[],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
                vararg=None,
                kwarg=None,
            ),
            body=[Return(value=set_value("Hello, webapp2!"))],
            decorator_list=[
                Call(
                    func=Attribute(
                        value=Name(id="app", ctx=Load()), attr="get", ctx=Load()
                    ),
                    args=[set_value("/")],
                    keywords=[],
                )
            ],
            returns=None,
            lineno=None,
            **maybe_type_comment
        ),
    ],
    type_ignores=[],
)


__all__ = ["hello_fastapi_mod", "hello_fastapi_str"]
