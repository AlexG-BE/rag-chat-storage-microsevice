from faker import Faker
from fastapi import status
from httpx import AsyncClient
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatSession
from app.schemas.chat_message import ChatMessageSchema
from tests.factories import ChatMessageFactory

test_url = "/api/sessions"


async def test_returns_chat_session_messages(
    client: AsyncClient,
    db_session: AsyncSession,
    chat_session: ChatSession,
):
    size = 3
    target_messages = await ChatMessageFactory.provide(db_session).create_batch(size=size, session=chat_session)
    _wrong_messages = await ChatMessageFactory.provide(db_session).create_batch(size=size)

    response = await client.get(f"{test_url}/{chat_session.id}/messages")

    assert response.status_code == status.HTTP_200_OK

    response_objs = TypeAdapter(list[ChatMessageSchema]).validate_python(response.json()["items"])
    assert len(response_objs) == size
    assert {i.id for i in response_objs} == {i.id for i in target_messages}
    assert [i.session_id == chat_session.id for i in response_objs]


async def test_returns_empty_list_if_messages_not_exist(
    client: AsyncClient,
    chat_session: ChatSession,
):
    response = await client.get(f"{test_url}/{chat_session.id}/messages")

    assert response.status_code == status.HTTP_200_OK
    assert not response.json()["items"]


async def test_returns_404_if_chat_session_not_exists(
    client: AsyncClient,
    faker: Faker,
):
    response = await client.get(f"{test_url}/{faker.uuid4()}/messages")

    assert response.status_code == status.HTTP_404_NOT_FOUND
