"""
Create migration scripts from NDB to SQLalchemy
"""

from ast import ClassDef, parse
from collections import deque
from functools import partial
from itertools import filterfalse
from operator import attrgetter, contains
from os import listdir, path

import cdd.sqlalchemy.parse
from cdd.shared.pure_utils import rpartial
from cdd.shared.source_transformer import to_code

from cdd_gae.ndb_sqlalchemy_migrator_utils import generate_ndb_to_sqlalchemy_mod


def generate_migration_file(
    ndb_class_def,
    sqlalchemy_class_def,
    ndb_mod_to_import,
    sqlalchemy_mod_to_import,
    output_file,
):
    """
    Generate migration file from NDB to SQLalchemy

    :param ndb_class_def: NDB class
    :type ndb_class_def: ```ClassDef```

    :param sqlalchemy_class_def: SQLalchemy class
    :type sqlalchemy_class_def: ```ClassDef```

    :param ndb_mod_to_import: NDB module name that the entity will be imported from
    :type ndb_mod_to_import: ```str```

    :param sqlalchemy_mod_to_import: SQLalchemy module name that the entity will be imported from
    :type sqlalchemy_mod_to_import: ```str```

    :param output_file: Output file
    :type output_file: ```str```
    """
    mod = generate_ndb_to_sqlalchemy_mod(
        name=ndb_class_def.name,
        fields=cdd.sqlalchemy.parse.sqlalchemy(sqlalchemy_class_def)["params"].keys(),
        ndb_mod_to_import=ndb_mod_to_import,
        sqlalchemy_mod_to_import=sqlalchemy_mod_to_import,
    )
    with open(output_file, "wt") as f:
        f.write(to_code(mod))


def ndb2sqlalchemy_migrator_folder(
    ndb_file,
    sqlalchemy_file,
    ndb_mod_to_import,
    sqlalchemy_mod_to_import,
    output_folder,
    dry_run=False,
):
    """
    Create migration scripts from NDB to SQLalchemy

    :param ndb_file: Python file containing the NDB `class`es
    :type ndb_file: ```str```

    :param sqlalchemy_file: Python file containing the NDB `class`es
    :type sqlalchemy_file: ```str```

    :param ndb_mod_to_import: NDB module name that the entity will be imported from
    :type ndb_mod_to_import: ```str```

    :param sqlalchemy_mod_to_import: SQLalchemy module name that the entity will be imported from
    :type sqlalchemy_mod_to_import: ```str```

    :param output_folder:  Empty folder to generate scripts that migrate from one NDB class to one SQLalchemy class
    :type output_folder: ```str```

    :param dry_run: Show what would be created; don't actually write to the filesystem
    :type dry_run: ```bool```
    """
    assert (
        path.isdir(output_folder) and len(listdir(output_folder)) == 0
    ), "{!r} must be empty and existent".format(output_folder)
    for f in ndb_file, sqlalchemy_file:
        assert path.isfile(f), "FileNotFound({!r})".format(f)
    if dry_run:
        print(
            "ndb2sqlalchemy_migrator_folder:",
            {
                "ndb_file": ndb_file,
                "sqlalchemy_file": sqlalchemy_file,
                "output_folder": output_folder,
                "dry_run": dry_run,
            },
        )
        return

    with open(sqlalchemy_file, "rt") as f:
        sqlalchemy_mod = parse(f.read())

    with open(ndb_file, "rt") as f:
        ndb_mod = parse(f.read())

    sqlalchemy_class_defs = dict(
        map(
            lambda cls_def: (cls_def.name, cls_def),
            filter(rpartial(isinstance, ClassDef), sqlalchemy_mod.body),
        )
    )

    entities = frozenset(map(attrgetter("name"), sqlalchemy_class_defs.values()))
    ndb_class_defs = dict(
        map(
            lambda cls_def: (cls_def.name, cls_def),
            filter(
                lambda cls_def: cls_def.name in entities,
                filter(rpartial(isinstance, ClassDef), ndb_mod.body),
            ),
        )
    )
    len_ndb_class_defs = len(ndb_class_defs)
    len_sqlalchemy_class_defs = len(sqlalchemy_class_defs)

    assert (
        len_ndb_class_defs == len_sqlalchemy_class_defs - 1
    ), "{} found SQLalchemy models != {} found NDB models, missing: {}".format(
        len_ndb_class_defs,
        len_sqlalchemy_class_defs,
        frozenset(ndb_class_defs.keys()) ^ frozenset(sqlalchemy_class_defs.keys()),
    )

    deque(
        map(
            lambda entity: generate_migration_file(
                ndb_class_defs[entity],
                sqlalchemy_class_defs[entity],
                ndb_mod_to_import,
                sqlalchemy_mod_to_import,
                output_file=path.join(
                    output_folder,
                    "{entity}{extsep}py".format(entity=entity, extsep=path.extsep),
                ),
            ),
            filterfalse(
                partial(
                    contains,
                    frozenset(ndb_class_defs.keys())
                    ^ frozenset(sqlalchemy_class_defs.keys()),
                ),
                entities,
            ),
        ),
        maxlen=0,
    )
    open(
        path.join(
            output_folder,
            "__init__{extsep}py".format(extsep=path.extsep),
        ),
        "a",
    ).close()


__all__ = ["ndb2sqlalchemy_migrator_folder"]
