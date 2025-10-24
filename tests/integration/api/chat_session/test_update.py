from faker import Faker
from fastapi import status
from httpx import AsyncClient

from app.models import ChatSession
from app.schemas.chat_session import ChatSessionDetailSchema

test_url = "/api/sessions"


async def test_update_returns_updated_chat_session(
    client: AsyncClient,
    faker: Faker,
    chat_session: ChatSession,
):
    initial_title = chat_session.title

    response = await client.patch(f"{test_url}/{chat_session.id}", json={"title": faker.pystr()})

    assert response.status_code == status.HTTP_200_OK

    response_obj = ChatSessionDetailSchema.model_validate(response.json())
    assert response_obj.title != initial_title


async def test_returns_422_if_schema_not_valid(
    client: AsyncClient,
    chat_session: ChatSession,
):
    response = await client.patch(f"{test_url}/{chat_session.id}", json={"title": None})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_update_returns_404_if_chat_session_not_exists(
    client: AsyncClient,
    faker: Faker,
):
    response = await client.patch(
        f"{test_url}/{faker.uuid4()}",
        json={
            "title": faker.pystr(),
            "is_favorite": faker.pybool(),
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
