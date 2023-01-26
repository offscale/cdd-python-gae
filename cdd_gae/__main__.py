#!/usr/bin/env python

"""
`__main__` implementation, can be run directly or with `python -m cdd_gae`
"""

from argparse import ArgumentParser
from importlib import import_module
from os import path

import cdd.gen_utils
import cdd.source_transformer
from cdd.__main__ import parse_emit_types

import cdd_gae.ndb2sqlalchemy
import cdd_gae.ndb2sqlalchemy_migrator
import cdd_gae.parquet2sqlalchemy
import cdd_gae.parse.ndb
import cdd_gae.parse.parquet
import cdd_gae.webapp2_to_fastapi
from cdd_gae import __description__, __version__


def _build_parser():
    """
    Parser builder

    :return: instanceof ArgumentParser
    :rtype: ```ArgumentParser```
    """
    parser = ArgumentParser(
        prog="python -m cdd_gae",
        description=__description__,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {__version__}".format(__version__=__version__),
    )

    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = "command"

    #######
    # gen #
    #######
    gen_parser = subparsers.add_parser(
        "gen", help="Go from cdd_gae supported parse type to cdd supported emit type"
    )
    gen_parser.add_argument(
        "--parse",
        help="What type the input is.",
        choices=("ndb", "parquet", "webapp2"),
        dest="parse_name",
    )
    gen_parser.add_argument(
        "--emit",
        help="What type to generate.",
        choices=parse_emit_types,
        required=True,
        dest="emit_name",
    )
    gen_parser.add_argument(
        "-i",
        "--input-file",
        help="Python file to parse NDB `class`es out of",
        required=True,
    )
    gen_parser.add_argument(
        "-o",
        "--output-file",
        help="Empty file to generate SQLalchemy classes to",
        required=True,
    )
    gen_parser.add_argument(
        "--name",
        help="Name of function/class to emit, defaults to inferring from filename",
    )
    gen_parser.add_argument(
        "--dry-run",
        help="Show what would be created; don't actually write to the filesystem.",
        action="store_true",
    )

    ###########################
    # ndb2sqlalchemy_migrator #
    ###########################
    ndb2sqlalchemy_migrator_parser = subparsers.add_parser(
        "ndb2sqlalchemy_migrator",
        help="Create migration scripts from NDB to SQLalchemy",
    )
    ndb2sqlalchemy_migrator_parser.add_argument(
        "--ndb-file",
        help="Python file containing the NDB `class`es",
        required=True,
    )
    ndb2sqlalchemy_migrator_parser.add_argument(
        "--sqlalchemy-file",
        help="Python file containing the NDB `class`es",
        required=True,
    )
    ndb2sqlalchemy_migrator_parser.add_argument(
        "--ndb-mod-to-import",
        help="NDB module name that the entity will be imported from",
        required=True,
    )
    ndb2sqlalchemy_migrator_parser.add_argument(
        "--sqlalchemy-mod-to-import",
        help="SQLalchemy module name that the entity will be imported from",
        required=True,
    )
    ndb2sqlalchemy_migrator_parser.add_argument(
        "-o",
        "--output-folder",
        help="Empty folder to generate scripts that migrate from one NDB class to one SQLalchemy class",
        required=True,
    )
    ndb2sqlalchemy_migrator_parser.add_argument(
        "--dry-run",
        help="Show what would be created; don't actually write to the filesystem.",
        action="store_true",
    )

    return parser


def main(cli_argv=None, return_args=False):
    """
    Run the CLI parser

    :param cli_argv: CLI arguments. If None uses `sys.argv`.
    :type cli_argv: ```Optional[List[str]]```

    :param return_args: Primarily use is for tests. Returns the args rather than executing anything.
    :type return_args: ```bool```

    :return: the args if `return_args`, else None
    :rtype: ```Optional[Namespace]```
    """
    _parser = _build_parser()
    args = _parser.parse_args(args=cli_argv)

    if return_args:
        return args

    command = args.command
    args_dict = {k: v for k, v in vars(args).items() if k != "command"}
    if command == "gen":
        require_file_existent(_parser, args_dict["input_file"], name="input-file")

        if args_dict["parse_name"] == "webapp2":
            assert args_dict["emit_name"] == "fastapi", '{} != "fastapi"'.format(
                args_dict["emit_name"]
            )
            for key in "parse_name", "emit_name", "name":
                del args_dict[key]
            return cdd_gae.webapp2_to_fastapi.webapp2_to_fastapi_file(**args_dict)

        ir = (
            {"parquet": cdd_gae.parse.parquet.parquet, "ndb": cdd_gae.parse.ndb.ndb}[
                args_dict["parse_name"]
            ]
        )(args_dict["input_file"], name=args_dict["name"])
        global__all__ = []
        mod = cdd.gen_utils.gen_module(
            decorator_list=[],
            emit_and_infer_imports=True,
            emit_call=True,
            emit_default_doc=True,
            emit_name=args_dict["emit_name"],
            functions_and_classes=(
                print("\nGenerating: {name!r}".format(name=ir["name"]))
                or global__all__.append(ir["name"])
                or (
                    getattr(
                        import_module(
                            ".".join(("cdd", "emit", args_dict["emit_name"]))
                        ),
                        args_dict["emit_name"],
                    )(
                        ir,
                        emit_default_doc=True,
                        word_wrap=True,
                        **cdd.gen_utils.get_emit_kwarg(
                            decorator_list=[],
                            emit_call=True,
                            emit_name=args_dict["emit_name"],
                            name_tpl="{name}",
                            name=ir["name"],
                        ),
                    ),
                )
            ),
            imports="",
            input_mapping_it=dict(),
            name_tpl="{name}",
            no_word_wrap=False,
            parse_name="",
            prepend=None,
            global__all__=global__all__,
        )
        with open(args_dict["output_file"], "wt") as f:
            f.write(cdd.source_transformer.to_code(mod))

    else:
        assert command == "ndb2sqlalchemy_migrator"
        return cdd_gae.ndb2sqlalchemy_migrator.ndb2sqlalchemy_migrator_folder(
            **args_dict
        )


def require_file_existent(_parser, filename, name):
    """
    Raise SystemExit(2) if filename is None or not found

    :param _parser: The argparse parser
    :type _parser: ```ArgumentParser```

    :param filename: The filename
    :type filename: ```Optional[str]```

    :param name: Argument name
    :type name: ```str```
    """
    if filename is None or not path.isfile(filename):
        _parser.error(
            "--{name} must be an existent file. Got: {filename!r}".format(
                name=name, filename=filename
            )
        )


if __name__ == "__main__":
    main()

__all__ = ["main"]
