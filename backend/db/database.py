import os

from sqlalchemy import create_engine
from sqlmodel import Session

DATABASE_FILENAME = "database.db"
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATABASE_FILENAME}")
if DATABASE_URL == f"sqlite:///{DATABASE_FILENAME}":
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# print(DATABASE_URL)
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
