"""
'Upgrade' WebApp2 to FastAPI with this shiny function
"""

from ast import (
    Assign,
    Attribute,
    Call,
    ClassDef,
    FunctionDef,
    ImportFrom,
    List,
    Load,
    Module,
    Name,
    Store,
    Tuple,
    alias,
    parse,
)
from collections import OrderedDict
from functools import partial
from itertools import chain
from operator import attrgetter, itemgetter

from cdd.ast_utils import get_value, maybe_type_comment, set_value
from cdd.pure_utils import rpartial
from cdd.source_transformer import to_code

from cdd_gae.webapp2_to_fastapi_utils import generate_route


def webapp2_to_fastapi_file(input_file, output_file, dry_run=False):
    """
    Parse WebApp2 classes file then emit FastAPI functions to potentially different file

    :param input_file: Python file to parse FastAPI `class`es out of
    :type input_file: ```str```

    :param output_file: Empty file to generate FastAPI functions to
    :type output_file: ```str```

    :param dry_run: Show what would be created; don't actually write to the filesystem
    :type dry_run: ```bool```
    """

    if dry_run:
        print("[webapp2_to_fastapi_file] Dry running")
        return

    with open(input_file, "rt") as f:
        src = f.read()

    fastapi_mod = webapp2_to_fastapi(parse(src))

    fastapi_mod.body.insert(
        0,
        ImportFrom(
            level=0,
            module="fastapi",
            names=[alias(asname=None, name="FastAPI")],
            lineno=None,
        ),
    )
    fastapi_mod.body.append(
        Assign(
            targets=[Name("__all__", Store())],
            value=List(
                ctx=Load(),
                elts=[set_value("app")],
                expr=None,
            ),
            expr=None,
            lineno=None,
            **maybe_type_comment,
        )
    )

    with open(output_file, "wt") as f:
        f.write(to_code(fastapi_mod))


def webapp2_to_fastapi(mod):
    """
    Convert WebApp2 to FastAPI

    :param mod: AST module containing WebApp2 routes and mapper function call
    :type mod: ```ast.Module```

    :returns: Equivalent AST module but for FastAPI
    :rtype: ```ast.Module```
    """
    if not mod.body:
        return mod

    routes_map = OrderedDict(
        map(
            lambda node: tuple(map(get_value, node.elts))[::-1]
            if isinstance(node, Tuple)
            else node,
            next(
                map(
                    attrgetter("elts"),
                    map(
                        itemgetter(0),
                        map(
                            attrgetter("args"),
                            filter(
                                lambda call: isinstance(call.func, Attribute)
                                and call.func.value.id == "webapp2"
                                and call.func.attr == "WSGIApplication",
                                filter(
                                    rpartial(isinstance, Call),
                                    map(
                                        attrgetter("value"),
                                        filter(rpartial(isinstance, Assign), mod.body),
                                    ),
                                ),
                            ),
                        ),
                    ),
                )
            ),
        )
    )

    return Module(
        body=list(
            chain.from_iterable(
                (
                    (
                        Assign(
                            targets=[Name(id="app", ctx=Store())],
                            value=Call(
                                func=Name(id="FastAPI", ctx=Load()),
                                args=[],
                                keywords=[],
                            ),
                            **maybe_type_comment,
                            expr=None,
                            lineno=None,
                        ),
                    ),
                    chain.from_iterable(
                        map(
                            lambda class_def: map(
                                partial(
                                    generate_route,
                                    uri=routes_map[class_def.name],
                                    cls_name=class_def.name,
                                ),
                                filter(
                                    lambda func: func.name
                                    in frozenset(
                                        (
                                            "delete",
                                            "get",
                                            "options",
                                            "patch",
                                            "post",
                                            "put",
                                        )
                                    ),
                                    filter(
                                        rpartial(isinstance, FunctionDef),
                                        class_def.body,
                                    ),
                                ),
                            ),
                            filter(rpartial(isinstance, ClassDef), mod.body),
                        ),
                    ),
                )
            )
        ),
        type_ignores=[],
    )


__all__ = ["webapp2_to_fastapi", "webapp2_to_fastapi_file"]
