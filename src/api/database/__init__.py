import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DATABASE_URL
from api.database._models import Base, questions_asked_table, Question, User


engine = create_async_engine(DATABASE_URL)

session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
asyncio.ensure_future(create_tables())


__all__ = [
    "session_maker",
    "questions_asked_table",
    "Question",
    "User",
]
