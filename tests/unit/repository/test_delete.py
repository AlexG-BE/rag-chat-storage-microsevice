import pytest
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.exceptions import NotFoundError
from tests.unit.fixtures import TestModel, TestRepository


async def test_creates_and_returns_model_object(
    db_session: AsyncSession,
    test_repository: TestRepository,
    test_object: TestModel,
):
    result = await test_repository.delete(obj_id=test_object.id)

    db_obj = await db_session.scalar(select(TestModel))

    assert not result
    assert not db_obj


async def test_creates_and_returns_uncommited_model_object_if_autocommit_false(
    db_session_maker,
    db_session: AsyncSession,
    test_repository: TestRepository,
    test_object: TestModel,
):
    result = await test_repository.delete(obj_id=test_object.id, autocommit=False)

    async with db_session_maker() as another_session:
        db_obj = await another_session.scalar(select(TestModel))

    assert not result
    assert db_obj.id == test_object.id


async def test_returns_not_found_error_if_model_object_not_exists(
    faker: Faker,
    test_repository: TestRepository,
):
    with pytest.raises(NotFoundError):
        await test_repository.delete(obj_id=faker.uuid4(cast_to=None))
