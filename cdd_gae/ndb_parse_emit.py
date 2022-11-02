"""
Module that holds a function that parses NDB then emits SQLalchemy
"""

from ast import Assign, ClassDef, List, Load, Module, Name, Store, parse
from functools import partial
from operator import attrgetter, itemgetter

from cdd import emit
from cdd.ast_utils import maybe_type_comment, set_value
from cdd.pure_utils import rpartial
from cdd.source_transformer import to_code

from cdd_gae import parser


def ndb_parse_emit_file(input_file, output_file, dry_run=False):
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
    sqlalchemy_mod = Module(
        body=list(
            map(
                partial(emit.sqlalchemy, emit_repr=False),
                filter(
                    itemgetter("params"),
                    map(
                        parser.ndb_class_def,
                        filter(rpartial(isinstance, ClassDef), mod.body),
                    ),
                ),
            )
        ),
        type_ignores=[],
        stmt=None,
    )
    all_ = Assign(
        targets=[Name("__all__", Store())],
        value=List(
            ctx=Load(),
            elts=list(map(set_value, map(attrgetter("name"), sqlalchemy_mod.body))),
            expr=None,
        ),
        expr=None,
        lineno=None,
        **maybe_type_comment
    )
    sqlalchemy_mod.body.append(all_)
    with open(output_file, "wt") as f:
        f.write(to_code(sqlalchemy_mod))


__all__ = ["ndb_parse_emit_file"]
