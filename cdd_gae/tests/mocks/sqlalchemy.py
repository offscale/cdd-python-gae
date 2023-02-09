"""
Mocks for Sqlalchemy
"""

sqlalchemy_class_file_str = """
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
"""

ndb_to_sqlalchemy_migration_file_str = """
from os import environ as environ
from google.cloud import ndb as ndb
from sqlalchemy import create_engine as create_engine
from sqlalchemy.orm import sessionmaker as sessionmaker
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

__all__ = ["sqlalchemy_class_file_str", "ndb_to_sqlalchemy_migration_file_str"]
