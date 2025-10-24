import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatMessage
from tests.factories import ChatMessageFactory


@pytest.fixture
async def chat_message(db_session: AsyncSession) -> ChatMessage:
    return await ChatMessageFactory.provide(db_session).create()
