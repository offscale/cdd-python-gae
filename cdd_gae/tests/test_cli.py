""" Tests for CLI (__main__.py) """

import os
from argparse import ArgumentParser
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from os.path import extsep
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from cdd import __description__, __version__
from cdd.__main__ import _build_parser
from cdd.pure_utils import PY3_8
from cdd.tests.utils_for_tests import run_cli_test, unittest_main

from cdd_gae.__main__ import main


class TestCli(TestCase):
    """Test class for __main__.py"""

    def test_build_parser(self) -> None:
        """Test that `_build_parser` produces a parser object"""
        parser = _build_parser()
        self.assertIsInstance(parser, ArgumentParser)
        self.assertEqual(parser.description, __description__)

    def test_version(self) -> None:
        """Tests CLI interface gives version"""
        run_cli_test(
            self,
            ["--version"],
            exit_code=0,
            output=__version__,
            output_checker=lambda output: output[output.rfind(" ") + 1 :][:-1],
        )

    def test_name_main(self) -> None:
        """Test the `if __name__ == '__main___'` block"""

        argparse_mock = MagicMock()

        loader = SourceFileLoader(
            "__main__",
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "__main__{extsep}py".format(extsep=extsep),
            ),
        )
        with patch("argparse.ArgumentParser._print_message", argparse_mock), patch(
            "sys.argv", []
        ), self.assertRaises(SystemExit) as e:
            loader.exec_module(module_from_spec(spec_from_loader(loader.name, loader)))
        self.assertEqual(e.exception.code, SystemExit(2).code)

        self.assertEqual(
            (lambda output: output[(output.rfind(" ") + 1) :][:-1])(
                (argparse_mock.call_args.args if PY3_8 else argparse_mock.call_args[0])[
                    0
                ]
            ),
            "command",
        )

    def test_version_args(self):
        """Tests that NotImplemented is raised"""
        self.assertDictEqual(
            {
                "command": "ndb2sqlalchemy",
                "input_file": __file__,
                "output_file": "nonexistent.py",
                "dry_run": False,
            },
            vars(
                main(
                    cli_argv=["ndb2sqlalchemy", "-i", __file__, "-o", "nonexistent.py"],
                    return_args=True,
                )
            ),
        )

    def test_main_is_called_correctly(self) -> None:
        """Tests that `main` is called correctly"""
        with TemporaryDirectory() as tmpdir, patch(
            "cdd_gae.ndb_parse_emit.ndb_parse_emit_file", new_callable=MagicMock
        ) as func:
            output_file = os.path.join(tmpdir, "out{extsep}py".format(extsep=extsep))
            main(
                cli_argv=["ndb2sqlalchemy", "-i", __file__, "-o", output_file],
            )
            self.assertTrue(func.called)
            self.assertEqual(func.call_count, 1)
            self.assertEqual(
                func.call_args,
                call(input_file=__file__, output_file=output_file, dry_run=False),
            )


unittest_main()
