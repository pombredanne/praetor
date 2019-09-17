from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func


class Base:

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())

    @classmethod
    def create(cls, db, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
        return obj

    @classmethod
    def ensure_obj(cls, db, key, **kwargs):
        try:
            obj = db.query(cls).filter_by(**key).one()
            for k, v in kwargs.items():
                if v is not None:
                    setattr(obj, k, v)
            return obj
        except NoResultFound:
            return cls.create(db, **key, **kwargs)


Base = declarative_base(cls=Base)
