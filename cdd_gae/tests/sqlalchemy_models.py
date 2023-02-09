
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
