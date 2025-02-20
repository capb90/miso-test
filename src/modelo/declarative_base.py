from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

IS_TEST = False

DB_URL = 'sqlite:///enForma.sqlite' if IS_TEST else 'sqlite:///enFormaTest.sqlite'

engine = create_engine(DB_URL,echo=IS_TEST)
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()