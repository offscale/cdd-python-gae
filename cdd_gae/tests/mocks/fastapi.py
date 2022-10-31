"""
FastAPI mocks that match those in webapp2.py
"""

from ast import (
    FunctionDef,
    arguments,
    Return,
    Name,
    Attribute,
    Call,
    Load,
    Assign,
    Module,
    Store,
)

from cdd.ast_utils import set_value

hello_fastapi_str = """
from fastapi import FastAPI

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
        ),
        FunctionDef(
            name="read_root",
            args=arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
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
        ),
    ],
    type_ignores=[],
)


__all__ = ["hello_fastapi_mod", "hello_fastapi_str"]
