from sqlmodel import create_engine
from fastapi import Depends
from sqlmodel import SQLModel, Session
from typing import Annotated
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(url=os.getenv("DATABASE_URL"))


def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Database Error: {e}")
        raise


"""
Provides a generator that yields a new database session.

This function creates a new SQLModel session using the configured
database engine and yields it for use in database operations.
The session is automatically closed after use.
"""


def get_session():
    try:
        with Session(engine) as session:
            yield session
        print("Database connection succesfull")
    except Exception as e:
        print(f"Database connection error: {e}")
        raise


SessionDep = Annotated[Session, Depends(get_session)]
