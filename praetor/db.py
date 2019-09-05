from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("postgresql://praetor:praetor@localhost")
Session = sessionmaker(bind=engine)
