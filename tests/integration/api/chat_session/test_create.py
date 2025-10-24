from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app.schemas.chat_session import ChatSessionDetailSchema

test_url = "/api/sessions"


async def test_creates_and_returns_chat_session(
    client: AsyncClient,
    faker: Faker,
):
    response = await client.post(
        test_url,
        json={
            "user_id": faker.uuid4(),
            "title": faker.pystr(),
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert ChatSessionDetailSchema.model_validate(response.json())


async def test_returns_422_if_schema_not_valid(
    client: AsyncClient,
    faker: Faker,
):
    response = await client.post(test_url, json={"title": faker.pybool()})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
