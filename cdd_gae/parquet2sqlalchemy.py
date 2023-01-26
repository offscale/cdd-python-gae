"""
Module that holds a function that parses Parquet then emits SQLalchemy
"""

from ast import Assign, List, Module, Name, Store

import cdd.emit.sqlalchemy
import cdd.parse.utils.sqlalchemy_utils
import cdd.source_transformer
from cdd.ast_utils import maybe_type_comment, set_value

import cdd_gae.parse.parquet


def parquet2sqlalchemy(input_file, output_file, dry_run=False):
    """
    Parse Parquet file then emit SQLalchemy `class`

    :param input_file: Parquet file
    :type input_file: ```str```

    :param output_file: Empty file to generate the SQLalchemy class to
    :type output_file: ```str```

    :param dry_run: Show what would be created; don't actually write to the filesystem
    :type dry_run: ```bool```
    """

    if dry_run:
        print("[parquet2sqlalchemy] Dry running")
        return

    sqlalchemy_class = cdd.emit.sqlalchemy.sqlalchemy(
        cdd_gae.parse.parquet.parquet(input_file), class_name="Table"
    )
    sqlalchemy_mod = Module(
        body=[
            cdd.parse.utils.sqlalchemy_utils.imports_from((sqlalchemy_class,)),
            sqlalchemy_class,
            Assign(
                targets=[Name("__all__", Store())],
                value=List([set_value(sqlalchemy_class.name)], Store()),
                expr=None,
                lineno=None,
                **maybe_type_comment,
            ),
        ],
        type_ignores=[],
        stmt=None,
    )

    with open(output_file, "wt") as f:
        f.write(cdd.source_transformer.to_code(sqlalchemy_mod))


__all__ = ["parquet2sqlalchemy"]
