from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app.models import ChatSession
from app.schemas.chat_session import ChatSessionDetailSchema

test_url = "/api/sessions"


async def test_returns_chat_session(
    client: AsyncClient,
    chat_session: ChatSession,
):
    response = await client.get(f"{test_url}/{chat_session.id}")

    assert response.status_code == status.HTTP_200_OK
    response_obj = ChatSessionDetailSchema.model_validate(response.json())
    assert response_obj == ChatSessionDetailSchema.model_validate(chat_session)


async def test_returns_404_if_chat_session_not_exists(
    client: AsyncClient,
    faker: Faker,
):
    response = await client.get(f"{test_url}/{faker.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
