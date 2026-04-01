import os
import urllib
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE = os.getenv("DATABASE")
DATABASE_URL = os.getenv("DATABASE_URL")
USERNAME = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")

safe_username = urllib.parse.quote_plus(USERNAME)
safe_password = urllib.parse.quote_plus(PASSWORD)

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{safe_username}:{safe_password}@{DATABASE_URL}/{DATABASE}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

@contextmanager
def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def async_get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()