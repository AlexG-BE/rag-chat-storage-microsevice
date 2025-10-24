from typing import AsyncGenerator

import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import config
from app.core.dependencies import get_db_session
from app.core.enums import AppEnvEnum
from app.core.models import Base

pytest_plugins = ["tests.fixtures", "tests.unit.fixtures"]


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Set up test database."""
    if config.env_name != AppEnvEnum.TEST:
        pytest.exit("Tests must be run with TEST environment")

    root_engine = create_async_engine(
        f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/postgres",
        isolation_level="AUTOCOMMIT",
    )

    async with root_engine.begin() as conn:
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{config.db.name}"'))
        await conn.execute(text(f'CREATE DATABASE "{config.db.name}"'))


@pytest.fixture(scope="session")
async def db_engine() -> AsyncEngine:
    return create_async_engine(config.db.pg_dsn, echo=config.db.echo)


@pytest.fixture(scope="session")
async def db_session_maker(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create database schema once for all tests."""
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await conn.run_sync(Base.metadata.create_all)

    return async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def db_session(db_engine, db_session_maker) -> AsyncGenerator[AsyncSession, None]:
    """Provide database session for tests."""
    tables = ",".join(f'"{table.name}"' for table in reversed(Base.metadata.sorted_tables))

    async with db_session_maker() as session:
        await session.execute(text(f"TRUNCATE {tables} RESTART IDENTITY;"))

        await session.commit()

        yield session


@pytest.fixture(scope="session")
def app_instance():
    """Create and provide a test app instance."""
    from app.app import create_app

    return create_app()


@pytest.fixture
async def client(
    app_instance: FastAPI,
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """Provide test client with configured dependencies."""
    app_instance.dependency_overrides[get_db_session] = lambda: db_session

    async with (
        AsyncClient(
            transport=ASGITransport(app=app_instance),
            base_url="http://test",
        ) as client,
    ):
        yield client


@pytest.fixture(scope="session")
async def api_key_headers() -> dict[str, str]:
    return {"X-API-KEY": config.API_KEY}


@pytest.fixture(scope="session")
async def wrong_api_key_headers(_session_faker: Faker) -> dict[str, str]:
    return {"X-API-KEY": _session_faker.pystr()}
