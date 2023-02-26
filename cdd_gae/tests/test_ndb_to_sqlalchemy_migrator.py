"""
Tests for migration scripts from NDB to SQLalchemy
"""

import ast
import os
from os.path import extsep
from tempfile import mkdtemp
from unittest import TestCase

from cdd.tests.utils_for_tests import run_ast_test, unittest_main

from cdd_gae import ndb2sqlalchemy_migrator
from cdd_gae.tests.mocks.ndb import ndb_file_model_str
from cdd_gae.tests.mocks.sqlalchemy import (
    ndb_to_sqlalchemy_migration_mod,
    sqlalchemy_class_file_str,
)


def populate_files(tempdir):
    """
    Populate files in the tempdir

    :param tempdir: Temporary directory
    :type tempdir: ```str````

    :return: ndb_file_name, sqlalchemy_file_name, empty_dir
    :rtype: ```Tuple[str, str, str]```
    """
    ndb_file_name = os.path.join(tempdir, "ndb_models{extsep}py".format(extsep=extsep))
    sqlalchemy_file_name = os.path.join(
        tempdir, "sqlalchemy_models{extsep}py".format(extsep=extsep)
    )
    empty_dir = os.path.join(tempdir, "empty_dir")
    os.mkdir(empty_dir)

    with open(ndb_file_name, "wt") as f:
        f.write(ndb_file_model_str)
    with open(sqlalchemy_file_name, "wt") as f:
        f.write(sqlalchemy_class_file_str)
    return ndb_file_name, sqlalchemy_file_name, empty_dir


class TestNDBToSqlalchemyMigrator(TestCase):
    """
    Tests whether ndb to Sqlalchemy methods work correctly
    """

    tempdir = None

    @classmethod
    def setUpClass(cls) -> None:
        """Construct temporary module for use by tests"""
        cls.tempdir = mkdtemp()
        temp_module_dir = os.path.join(cls.tempdir, "gen_test_module")
        os.mkdir(temp_module_dir)
        (cls.ndb_file_name, cls.sqlalchemy_file_name, cls.empty_dir) = populate_files(
            temp_module_dir
        )

    def test_ndb_sqlalchemy_migrator(self) -> None:
        """
        Test the `ndb_sqlalchemy_migrator`
        """
        output_filename = os.path.join(
            self.empty_dir, "Person{extsep}py".format(extsep=extsep)
        )
        ndb2sqlalchemy_migrator.ndb2sqlalchemy_migrator_folder(
            self.ndb_file_name,
            self.sqlalchemy_file_name,
            "example_ndb",
            "example_sql",
            self.empty_dir,
        )
        with open(output_filename, "rt") as f:
            gen_module_str = f.read()
        run_ast_test(
            self,
            gen_ast=ast.parse(gen_module_str),
            gold=ndb_to_sqlalchemy_migration_mod,
        )


unittest_main()
