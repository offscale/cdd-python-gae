"""
Tests for migration scripts from NDB to SQLalchemy
"""
from unittest import TestCase
from tempfile import mkdtemp
import os
class TestNDB2SqlalchemyMigrator(TestCase):
    """
    Tests whether ndb to Sqlalchemy methods work correctly
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Construct temporary module for use by tests"""
        cls.tempdir = mkdtemp()
        temp_module_dir = os.path.join(cls.tempdir, "gen_test_module")
