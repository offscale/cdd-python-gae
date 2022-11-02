"""
Utility functions for webapp2_to_fastapi.py
"""

from ast import (
    Attribute,
    Call,
    FunctionDef,
    Load,
    Name,
    NodeTransformer,
    Return,
    arguments,
)

from cdd.ast_utils import maybe_type_comment, set_value


def generate_route(func, uri, cls_name):
    """
    Generate a FastAPI route from a WebApp2 route

    :param func: The original WebApp2 method
    :type func: ```FunctionDef```

    :param uri: URI for the route
    :type uri: ```str```

    :param cls_name: The WebApp2 class name
    :type cls_name: ```str```

    :returns: The new FastAPI route
    :rtype: ```FunctionDef```
    """
    return FunctionDef(
        name="_".join((cls_name, func.name)),
        args=arguments(
            posonlyargs=[],
            args=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None,
        ),
        body=RewriteResponse().visit(func).body,
        decorator_list=[
            Call(
                func=Attribute(
                    value=Name(id="app", ctx=Load()), attr=func.name, ctx=Load()
                ),
                args=[set_value(uri)],
                keywords=[],
            )
        ],
        returns=None,
        lineno=None,
        **maybe_type_comment
    )


class RewriteResponse(NodeTransformer):
    """
    Replace `self.response.write("")` with `return ""`
    """

    def visit_Expr(self, node):
        """
        visits the `Expr`, if it's the right one, replace it with a `Return`

        :param node: `Expr` of any sort
        :type node: ```Expr```

        :return: Either original `Expr` or a `Return`
        :rtype: ```Union[Expr,Return]```
        """
        if (
            isinstance(node.value, Call)
            and isinstance(node.value.func, Attribute)
            and isinstance(node.value.func.value, Attribute)
            and isinstance(node.value.func.value.value, Name)
            and node.value.func.value.value.id == "self"
            and node.value.func.value.attr == "response"
            and node.value.func.attr == "write"
        ):
            return Return(
                value=node.value.args[0]
                if len(node.value.args) == 1
                else node.value.args
            )

        return node


__all__ = ["generate_route"]
