#!/usr/bin/env python

"""
`__main__` implementation, can be run directly or with `python -m cdd_gae`
"""
from argparse import ArgumentParser
from os import path

from cdd_gae import __description__, __version__
from cdd_gae.ndb_parse_emit import ndb_parse_emit_file
from cdd_gae.webapp2_to_fastapi import webapp2_to_fastapi_file


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
    # ndb #
    #######
    ndb_parser = subparsers.add_parser(
        "ndb2sqlalchemy",
        help="Parse NDB emit SQLalchemy",
    )
    ndb_parser.add_argument(
        "-i",
        "--input-file",
        help="Python file to parse NDB `class`es out of",
        required=True,
    )
    ndb_parser.add_argument(
        "-o",
        "--output-file",
        help="Empty file to generate SQLalchemy classes to",
        required=True,
    )
    ndb_parser.add_argument(
        "--dry-run",
        help="Show what would be created; don't actually write to the filesystem.",
        action="store_true",
    )

    ######################
    # webapp2_to_fastapi #
    ######################
    ndb_parser = subparsers.add_parser(
        "webapp2_to_fastapi",
        help="Parse WebApp2 emit FastAPI",
    )
    ndb_parser.add_argument(
        "-i",
        "--input-file",
        help="Python file to parse WebApp2 `class`es out of",
        required=True,
    )
    ndb_parser.add_argument(
        "-o",
        "--output-file",
        help="Empty file to generate FastAPI functions to",
        required=True,
    )
    ndb_parser.add_argument(
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
    assert command in frozenset(("ndb2sqlalchemy", "webapp2_to_fastapi"))
    require_file_existent(_parser, args_dict["input_file"], name="input-file")

    return (
        webapp2_to_fastapi_file
        if command == "webapp2_to_fastapi"
        else ndb_parse_emit_file
    )(**args_dict)


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
