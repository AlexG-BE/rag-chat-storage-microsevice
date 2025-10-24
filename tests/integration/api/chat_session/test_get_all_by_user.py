from faker import Faker
from fastapi import status
from httpx import AsyncClient
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat_session import ChatSessionSchema
from tests.factories import ChatSessionFactory

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


async def test_returns_sessions_by_user_id(
    client: AsyncClient,
    db_session: AsyncSession,
    api_key_headers: dict,
    faker: Faker,
):
    size = 3
    user_id = faker.uuid4()
    target_sessions = await ChatSessionFactory.provide(db_session).create_batch(size=size, user_id=user_id)
    _wrong_sessions = await ChatSessionFactory.provide(db_session).create_batch(size=size)

    response = await client.get(test_url, params={"user_id": user_id}, headers=api_key_headers)

    assert response.status_code == status.HTTP_200_OK

    response_objs = TypeAdapter(list[ChatSessionSchema]).validate_python(response.json()["items"])
    assert len(response_objs) == size
    assert {i.id for i in response_objs} == {i.id for i in target_sessions}


async def test_returns_empty_list_if_user_id_not_exists(
    client: AsyncClient,
    api_key_headers: dict,
    faker: Faker,
):
    response = await client.get(test_url, params={"user_id": faker.uuid4()}, headers=api_key_headers)

    assert response.status_code == status.HTTP_200_OK
    assert not response.json()["items"]


async def test_returns_422_if_user_id_not_provided(
    client: AsyncClient,
    api_key_headers: dict,
):
    response = await client.get(test_url, headers=api_key_headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
