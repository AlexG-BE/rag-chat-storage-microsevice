from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import SenderTypeEnum
from app.models import ChatSession
from app.schemas.chat_message import ChatMessageSchema

test_url = "/api/sessions"


async def test_creates_and_returns_message(
    client: AsyncClient,
    db_session: AsyncSession,
    faker: Faker,
    chat_session: ChatSession,
):
    response = await client.post(
        f"{test_url}/{chat_session.id}/messages",
        json={
            "session_id": faker.uuid4(),  # should be ignored
            "sender": faker.enum(SenderTypeEnum),
            "content": faker.pystr(),
            "context": faker.pydict(value_types=(str,)),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_obj = ChatMessageSchema.model_validate(response.json())
    assert response_obj.session_id == chat_session.id


async def test_returns_404_if_chat_session_not_exists(
    client: AsyncClient,
    faker: Faker,
):
    response = await client.post(
        f"{test_url}/{faker.uuid4()}/messages",
        json={
            "session_id": faker.uuid4(),  # should be ignored
            "sender": faker.enum(SenderTypeEnum),
            "content": faker.pystr(),
            "context": faker.pydict(value_types=(str,)),
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
