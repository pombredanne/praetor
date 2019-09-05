from sqlalchemy.engine import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer


engine = create_engine('sqlite:///db.sqlite', echo=True)


Base = declarative_base()


class Flow(Base):

    __tablename__ = 'flow'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    state = Column(String)


Base.metadata.create_all(engine)
