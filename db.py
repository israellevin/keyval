#!/usr/bin/python3

# Default local db for testing, set the env variable to override.
dbfilename = 'keyval.db'
dbscheme = 'sqlite'
from os import environ
dburl = environ.get('DATABASE_URL', "%s:///%s" % (dbscheme, dbfilename))

from sqlalchemy import create_engine, event, exc, Column, String
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
engine = create_engine(dburl)
session = scoped_session(sessionmaker(bind = engine))
@event.listens_for(mapper, 'init')
def auto_add(target, args, kwargs):
    session.add(target)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Base.query = session.query_property()

class Value(Base):
    __tablename__ = 'values'
    key = Column(String, primary_key=True)
    value = Column(String)

    def __init__(self, key, value):
        self.key, self.value = key, value
        session.commit()

    @classmethod
    def getbykey(cls, key):
        try: return session.query(cls).filter_by(key=key).one()
        except exc.SQLAlchemyError: return None

    @classmethod
    def getall(cls):
        return session.query(cls).all()

if __name__ == '__main__':
    from os.path import isfile
    if isfile(dbfilename):
        if 'y' != input('Delete database and create a new one? (y/N): '):
            from sys import exit
            exit(0)
        from os import remove
        remove(dbfilename)
    Base.metadata.create_all(bind=engine)
