from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def create_context(is_test: bool = False):
    DB_URL = 'sqlite:///db_app.sqlite'
    if is_test:
        DB_URL = 'sqlite:///db_test.sqlite'
    engine = create_engine(DB_URL, echo=is_test)
    Session = sessionmaker(bind=engine)

    base = Base
    session = Session()

    return engine,base,session
