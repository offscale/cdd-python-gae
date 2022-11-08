""" Tests for CLI webapp2_to_fastapi subparser (__main__.py) """

from unittest import TestCase
from unittest.mock import patch

from cdd.tests.utils_for_tests import mock_function, run_cli_test, unittest_main

from cdd_gae import __main__


class Testwebapp2_to_fastapi(TestCase):
    """Test class for __main__.py"""

    def test_webapp2_to_fastapi_wrong_args(self) -> None:
        """Tests CLI interface wrong args failure case"""

        with patch("cdd.__main__.main", __main__.main):
            run_cli_test(
                self,
                ["webapp2_to_fastapi", "--wrong"],
                exit_code=2,
                output="the following arguments are required: -i/--input-file, -o/--output-file\n",
            )

    def test_webapp2_to_fastapi_fails_with_file_missing(self) -> None:
        """Tests CLI interface file missing failure case"""

        with patch("cdd_gae.__main__", mock_function), patch(
            "cdd.__main__.main", __main__.main
        ):
            self.assertTrue(
                run_cli_test(
                    self,
                    [
                        "webapp2_to_fastapi",
                        "-i",
                        "foo",
                        "-o",
                        "bar",
                        "--dry-run",
                    ],
                    exit_code=2,
                    output="--input-file must be an existent file. Got: 'foo'\n",
                ),
            )

    # def test_doctrans_succeeds(self) -> None:
    #     """Tests CLI interface gets all the way to the doctrans call without error"""
    #
    #     with TemporaryDirectory() as tempdir:
    #         filename = path.join(tempdir, "foo")
    #         open(filename, "a").close()
    #         with patch("cdd.__main__.doctrans", mock_function):
    #             self.assertTrue(
    #                 run_cli_test(
    #                     self,
    #                     [
    #                         "doctrans",
    #                         "--filename",
    #                         filename,
    #                         "--format",
    #                         "numpydoc",
    #                         "--type-annotations",
    #                     ],
    #                     exit_code=None,
    #                     output=None,
    #                 ),
    #             )


unittest_main()
