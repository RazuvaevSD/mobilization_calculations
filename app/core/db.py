from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from .settings import DB_URI

Base = declarative_base()

engine = create_engine(DB_URI)

session = Session(bind=engine)
