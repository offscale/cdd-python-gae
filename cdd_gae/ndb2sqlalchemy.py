"""
Module that holds a function that parses NDB then emits SQLalchemy
"""

from ast import (
    Assign,
    Call,
    ClassDef,
    ImportFrom,
    List,
    Load,
    Module,
    Name,
    Store,
    alias,
    parse,
)
from collections import deque
from functools import partial
from itertools import chain
from operator import itemgetter

import cdd.emit.sqlalchemy
from cdd.ast_utils import get_value, maybe_type_comment, set_value
from cdd.pure_utils import rpartial
from cdd.source_transformer import to_code

from cdd_gae import parser


def ndb2sqlalchemy(input_file, output_file, dry_run=False):
    """
    Parse NDB classes file then emit SQLalchemy classes to potentially different file

    :param input_file: Python file to parse NDB `class`es out of
    :type input_file: ```str```

    :param output_file: Empty file to generate SQLalchemy classes to
    :type output_file: ```str```

    :param dry_run: Show what would be created; don't actually write to the filesystem
    :type dry_run: ```bool```
    """

    if dry_run:
        print("[ndb_parse_emit_file] Dry running")
        return

    with open(input_file, "rt") as f:
        src = f.read()
    mod = parse(src)

    sqlalchemy_imports = frozenset(
        (
            "Boolean",
            "Date",
            "DateTime",
            "Enum",
            "Float",
            "Identity",
            "Integer",
            "Interval",
            "JSON",
            "Numeric",
            "String",
            "Text",
            "Time",
            "Unicode",
        )
    )
    sqlalchemy_mod = Module(
        body=list(
            chain.from_iterable(
                (
                    (
                        ImportFrom(
                            module="sqlalchemy.orm",
                            names=[
                                alias(
                                    name="declarative_base",
                                    asname=None,
                                    identifier=None,
                                    identifier_name=None,
                                )
                            ],
                            level=0,
                        ),
                        ImportFrom(
                            module="sqlalchemy",
                            names=[],
                            level=0,
                        ),
                        Assign(
                            targets=[Name(id="Base", ctx=Store())],
                            value=Call(
                                func=Name(id="declarative_base", ctx=Load()),
                                args=[],
                                keywords=[],
                            ),
                            expr=None,
                            lineno=None,
                            **maybe_type_comment
                        ),
                    ),
                    map(
                        partial(cdd.emit.sqlalchemy.sqlalchemy, emit_repr=False),
                        filter(
                            itemgetter("params"),
                            map(
                                parser.ndb_class_def,
                                filter(rpartial(isinstance, ClassDef), mod.body),
                            ),
                        ),
                    ),
                    (
                        Assign(
                            targets=[Name("__all__", Store())],
                            value=None,
                            expr=None,
                            lineno=None,
                            **maybe_type_comment
                        ),
                    ),
                )
            )
        ),
        type_ignores=[],
        stmt=None,
    )
    types = set()
    # Figure out what is used for the `from sqlalchemy import <>` expression
    sqlalchemy_mod.body[-1].value = List(
        ctx=Load(),
        elts=list(
            map(
                set_value,
                map(
                    lambda cls_def: deque(
                        map(
                            types.add,
                            map(
                                lambda call: deque(
                                    map(
                                        types.add,
                                        map(
                                            lambda keyword: keyword.value.func.id,
                                            filter(
                                                lambda keyword: keyword.arg
                                                in frozenset(
                                                    ("default", "server_default")
                                                )
                                                and isinstance(keyword.value, Call),
                                                call.keywords,
                                            ),
                                        ),
                                    ),
                                    maxlen=0,
                                )
                                or call.args[0].id,
                                map(
                                    get_value,
                                    filter(
                                        lambda node: isinstance(node, Assign)
                                        and isinstance(node.value, Call),
                                        cls_def.body,
                                    ),
                                ),
                            ),
                        ),
                        maxlen=0,
                    )
                    or cls_def.name,
                    filter(rpartial(isinstance, ClassDef), sqlalchemy_mod.body),
                ),
            )
        ),
        expr=None,
    )
    sqlalchemy_mod.body[1].names = list(
        map(
            lambda sql_type: alias(
                name=sql_type,
                asname=None,
                identifier=None,
                identifier_name=None,
            ),
            sorted(types & sqlalchemy_imports | {"Column"}),
        )
    )
    with open(output_file, "wt") as f:
        f.write(to_code(sqlalchemy_mod))


__all__ = ["ndb2sqlalchemy"]
