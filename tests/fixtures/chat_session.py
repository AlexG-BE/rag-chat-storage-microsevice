import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatSession
from tests.factories import ChatSessionFactory


@pytest.fixture
async def chat_session(db_session: AsyncSession) -> ChatSession:
    return await ChatSessionFactory.provide(db_session).create()
