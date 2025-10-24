from faker import Faker
from fastapi import status
from httpx import AsyncClient

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


async def test_creates_and_returns_chat_session(
    client: AsyncClient,
    api_key_headers: dict,
    faker: Faker,
):
    response = await client.post(
        test_url,
        json={
            "user_id": faker.uuid4(),
            "title": faker.pystr(),
        },
        headers=api_key_headers,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert ChatSessionDetailSchema.model_validate(response.json())


async def test_returns_422_if_schema_not_valid(
    client: AsyncClient,
    api_key_headers: dict,
    faker: Faker,
):
    response = await client.post(test_url, json={"title": faker.pybool()}, headers=api_key_headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
