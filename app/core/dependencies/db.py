from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import config

engine = create_async_engine(
    config.db.pg_dsn,
    pool_size=15,
    max_overflow=15,
    echo=config.db.echo,
)


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session(
    session_maker: Annotated[async_sessionmaker[AsyncSession], Depends(get_session_maker)],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
