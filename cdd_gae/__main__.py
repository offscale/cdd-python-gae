#!/usr/bin/env python

"""
`__main__` implementation, can be run directly or with `python -m cdd`
"""

from argparse import ArgumentParser, Namespace
from codecs import decode
from collections import deque
from itertools import filterfalse
from operator import eq
from os import path

from cdd import __description__, __version__
from cdd.conformance import ground_truth
from cdd.docstring_parsers import Style
from cdd.doctrans import doctrans
from cdd.exmod import exmod
from cdd.gen import gen
from cdd.openapi.gen_openapi import openapi_bulk
from cdd.openapi.gen_routes import gen_routes, upsert_routes
from cdd.pure_utils import pluralise, rpartial
from cdd.sync_properties import sync_properties


def _build_parser():
    """
    Parser builder

    :return: instanceof ArgumentParser
    :rtype: ```ArgumentParser```
    """
    parser = ArgumentParser(
        prog="python -m cdd",
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

    parse_emit_types = ("ndb",)

    #########
    # ndb #
    #########
    ndb_parser = subparsers.add_parser(
        "ndb",
        help=("ndb parser"),
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
    command = args.command
    args_dict = {k: v for k, v in vars(args).items() if k != "command"}
    if command == "sync":
        args = Namespace(
            **{
                k: v
                if k in frozenset(("truth", "no_word_wrap"))
                or isinstance(v, list)
                or v is None
                else [v]
                for k, v in args_dict.items()
            }
        )

        truth_file = getattr(args, pluralise(args.truth))
        require_file_existent(
            _parser, truth_file[0] if truth_file else truth_file, name="truth"
        )
        truth_file = path.realpath(path.expanduser(truth_file[0]))

        number_of_files = sum(
            len(val)
            for key, val in vars(args).items()
            if isinstance(val, list) and not key.endswith("_names")
        )

        if number_of_files < 2:
            _parser.error(
                "Two or more of `--argparse-function`, `--class`, and `--function` must"
                " be specified"
            )
        require_file_existent(_parser, truth_file, name="truth")

        return args if return_args else ground_truth(args, truth_file)
    elif command == "sync_properties":
        deque(
            (
                setattr(
                    args, fname, path.realpath(path.expanduser(getattr(args, fname)))
                )
                for fname in ("input_filename", "output_filename")
                if path.isfile(getattr(args, fname))
            ),
            maxlen=0,
        )

        for filename, arg_name in (args.input_filename, "input-file"), (
            args.output_filename,
            "output-file",
        ):
            require_file_existent(_parser, filename, name=arg_name)
        sync_properties(**args_dict)
    elif command == "gen":
        if path.isfile(args.output_filename):
            raise IOError(
                "File exists and this is a destructive operation. Delete/move {output_filename!r} then"
                " rerun.".format(output_filename=args.output_filename)
            )
        gen(**args_dict)
    elif command == "gen_routes":
        if args.route is None:
            args.route = "/api/{model_name}".format(model_name=args.model_name.lower())

        (
            lambda routes__primary_key: upsert_routes(
                app=args.app_name,
                route=args.route,
                routes=routes__primary_key[0],
                routes_path=getattr(args, "routes_path", None),
                primary_key=routes__primary_key[1],
            )
        )(
            gen_routes(
                app=args.app_name,
                crud=args.crud,
                model_name=args.model_name,
                model_path=args.model_path,
                route=args.route,
            )
        )
    elif command == "openapi":
        openapi_bulk(**args_dict)
    elif command == "doctrans":
        require_file_existent(_parser, args.filename, name="filename")
        args_dict["docstring_format"] = args_dict.pop("format")
        doctrans(**args_dict)
        # except:
        #     import sys
        #     print("#", args_dict["filename"], file=sys.stderr)
        #     raise
    elif command == "exmod":
        exmod(
            mock_imports=False,  # This option is really only useful for tests IMHO
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
