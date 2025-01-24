from sqlalchemy import create_engine
from sqlmodel import Session

from models.sqlmodels import *

DATABASE_FILENAME = "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILENAME}"

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
