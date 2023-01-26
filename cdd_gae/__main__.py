#!/usr/bin/env python

"""
`__main__` implementation, can be run directly or with `python -m cdd_gae`
"""

from argparse import ArgumentParser
from os import path

import cdd_gae.ndb2sqlalchemy
import cdd_gae.ndb2sqlalchemy_migrator
import cdd_gae.parquet2sqlalchemy
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

    ##################
    # ndb2sqlalchemy #
    ##################
    ndb2sqlalchemy_parser = subparsers.add_parser(
        "ndb2sqlalchemy",
        help="Parse NDB emit SQLalchemy",
    )
    ndb2sqlalchemy_parser.add_argument(
        "-i",
        "--input-file",
        help="Python file to parse NDB `class`es out of",
        required=True,
    )
    ndb2sqlalchemy_parser.add_argument(
        "-o",
        "--output-file",
        help="Empty file to generate SQLalchemy classes to",
        required=True,
    )
    ndb2sqlalchemy_parser.add_argument(
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

    ######################
    # parquet2sqlalchemy #
    ######################
    parquet2sqlalchemy_parser = subparsers.add_parser(
        "parquet2sqlalchemy",
        help="Parse Parquet emit SQLalchemy",
    )
    parquet2sqlalchemy_parser.add_argument(
        "-i",
        "--input-file",
        help="Parquet filepath",
        required=True,
    )
    parquet2sqlalchemy_parser.add_argument(
        "-o",
        "--output-file",
        help="Empty file to generate SQLalchemy classes to",
        required=True,
    )
    parquet2sqlalchemy_parser.add_argument(
        "--dry-run",
        help="Show what would be created; don't actually write to the filesystem.",
        action="store_true",
    )

    ######################
    # webapp2_to_fastapi #
    ######################
    webapp2_to_fastapi_parser = subparsers.add_parser(
        "webapp2_to_fastapi",
        help="Parse WebApp2 emit FastAPI",
    )
    webapp2_to_fastapi_parser.add_argument(
        "-i",
        "--input-file",
        help="Python file to parse WebApp2 `class`es out of",
        required=True,
    )
    webapp2_to_fastapi_parser.add_argument(
        "-o",
        "--output-file",
        help="Empty file to generate FastAPI functions to",
        required=True,
    )
    webapp2_to_fastapi_parser.add_argument(
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
    if command in frozenset(
        ("ndb2sqlalchemy", "parquet2sqlalchemy", "webapp2_to_fastapi")
    ):
        require_file_existent(_parser, args_dict["input_file"], name="input-file")

        return (
            {
                "ndb2sqlalchemy": cdd_gae.ndb2sqlalchemy.ndb2sqlalchemy,
                "parquet2sqlalchemy": cdd_gae.parquet2sqlalchemy.parquet2sqlalchemy,
                "webapp2_to_fastapi": cdd_gae.webapp2_to_fastapi.webapp2_to_fastapi_file,
            }[command]
        )(**args_dict)
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
