from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


DB_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/shopdb"
engine = create_async_engine(url=DB_URL)

session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
