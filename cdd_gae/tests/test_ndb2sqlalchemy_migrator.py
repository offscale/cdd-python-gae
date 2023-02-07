"""
Tests for migration scripts from NDB to SQLalchemy
"""
from unittest import TestCase
from cdd_gae import ndb2sqlalchemy_migrator
import os
from os.path import extsep
from shutil import rmtree

class TestNDB2SqlalchemyMigrator(TestCase):
    """
    Tests whether ndb to Sqlalchemy methods work correctly
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Construct temporary module for use by tests"""
        os.mkdir("empty_dir")
        ndb_file_name = os.path.join("ndb_models{extsep}py".format(extsep=extsep))
        sqlalchemy_file_name = os.path.join("sqlalchemy_models{extsep}py".format(extsep=extsep))
        ndb_model_code = """
from google.appengine.ext import ndb

class Person(ndb.Model):
  name = ndb.StringProperty()
  age = ndb.IntegerProperty()
        """
        sqlalchemy_model_code = """
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()

# an example mapping using the base
class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

class Hero(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
        """
        with open(ndb_file_name, "wt") as f:
            f.write(ndb_model_code)
        with open(sqlalchemy_file_name, "wt") as f:
            f.write(sqlalchemy_model_code)

    @classmethod
    def tearDownClass(cls) -> None:
        """Drop the new module from the path and delete the temporary directory"""
        # sys.path = cls.sys_path
        rmtree("empty_dir")
        os.remove("ndb_models.py")
        os.remove("sqlalchemy_models.py")

    def test_ndb_sqlalchemy_migrator(self) -> None:
        ndb2sqlalchemy_migrator.ndb2sqlalchemy_migrator_folder("ndb_models.py",
                                                               "sqlalchemy_models.py", "example_ndb", "example_sql",
                                                               "empty_dir")
        with open('empty_dir/Person.py', 'r') as file:
            output = file.read()
        expected_output = """from os import environ as environ
from google.cloud import ndb as ndb
from sqlalchemy import create_engine as environ
from sqlalchemy.orm import sessionmaker as environ
from example_ndb import Person as NDB_Person
from example_sql import Person as SQL_Person
if __name__ == '__main__':
    ndb_client = ndb.Client()
    ndb_context = ndb_client.context()
    ndb_context.set_cache_policy(False)
    engine = create_engine(environ['RDBMS_URI'])
    Session = sessionmaker(bind=engine)
    SQL_Person.metadata.create_all(engine)
    session = Session()
    query = NDB_Person.query()
    entity_no = 0
    batch_size = 20
    for ndb_entity in query.fetch(offset=0, batch_size=batch_size):
        new_sql_entity = SQL_Person(name=ndb_entity.name, fullname=
            ndb_entity.fullname, nickname=ndb_entity.nickname)
        session.add(new_sql_entity)
    print('Committing', entity_no, 'Person')
    session.commit()
"""
        self.assertEqual(output, expected_output)
