from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatMessage, ChatSession
from tests.factories import ChatMessageFactory

test_url = "/api/sessions"


async def test_delete_returns_204_if_chat_session_deleted(
    client: AsyncClient,
    db_session: AsyncSession,
    chat_session: ChatSession,
):
    # Create ChatMessages assigned to target ChatSession
    await ChatMessageFactory.provide(db_session).create_batch(size=3, session=chat_session)

    # Create ChatMessage assigned to another ChatSession
    other_message = await ChatMessageFactory.provide(db_session).create()

    response = await client.delete(f"{test_url}/{chat_session.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check that only target ChatSession deleted
    chat_sessions = (await db_session.scalars(select(ChatSession))).all()
    assert len(chat_sessions) == 1
    assert chat_sessions[0].id == other_message.session_id

    # Check that only assigned ChatMessages deleted
    chat_messages = (await db_session.scalars(select(ChatMessage))).all()
    assert len(chat_messages) == 1
    assert chat_messages[0].id == other_message.id


async def test_delete_returns_404_if_chat_session_not_exists(
    client: AsyncClient,
    faker: Faker,
):
    response = await client.delete(f"{test_url}/{faker.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
