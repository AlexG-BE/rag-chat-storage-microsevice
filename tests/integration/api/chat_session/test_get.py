from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app.models import ChatSession
from app.schemas.chat_session import ChatSessionDetailSchema

test_url = "/api/sessions"


async def test_return_403_if_provided_wrong_api_key(
    client: AsyncClient,
    wrong_api_key_headers: dict,
):
    response = await client.post(test_url, headers=wrong_api_key_headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_return_422_if_provided_proper_api_key(
    client: AsyncClient,
    api_key_headers: dict,
):
    response = await client.post(test_url, headers=api_key_headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


async def test_returns_chat_session(
    client: AsyncClient,
    api_key_headers: dict,
    chat_session: ChatSession,
):
    response = await client.get(f"{test_url}/{chat_session.id}", headers=api_key_headers)

    assert response.status_code == status.HTTP_200_OK
    response_obj = ChatSessionDetailSchema.model_validate(response.json())
    assert response_obj == ChatSessionDetailSchema.model_validate(chat_session)


async def test_returns_404_if_chat_session_not_exists(
    client: AsyncClient,
    api_key_headers: dict,
    faker: Faker,
):
    response = await client.get(f"{test_url}/{faker.uuid4()}", headers=api_key_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
