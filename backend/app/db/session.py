import os
import urllib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE = os.getenv("DATABASE")
DATABASE_URL = os.getenv("DATABASE_URL")
USERNAME = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")

safe_username = urllib.parse.quote_plus(USERNAME)
safe_password = urllib.parse.quote_plus(PASSWORD)

SQLALCHEMY_DATABASE_URL = f"postgresql://{safe_username}:{safe_password}@{DATABASE_URL}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()