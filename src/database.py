
from collections.abc import AsyncGenerator
from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .settings import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_PORT, DB_DRIVER

DATABASE_URL = f"{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

Base = declarative_base()

async_engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session() as session:
        yield session
