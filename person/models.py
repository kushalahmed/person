from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, CHAR
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
Session = sessionmaker()

class Person(Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(length=255), nullable=False)
    surname = Column(String(length=255))
    date_of_birth = Column(Date, nullable=False)
    sex = Column(CHAR(length=1))
    email = Column(String(length=255), nullable=False)