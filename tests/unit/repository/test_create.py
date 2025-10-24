from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.fixtures import TestModel, TestRepository


async def test_creates_and_returns_model_object(
    db_session: AsyncSession,
    faker: Faker,
    test_repository: TestRepository,
):
    result: TestModel = await test_repository.create(obj_data={"title": faker.pystr()})

    db_obj = await db_session.scalar(select(TestModel))

    assert result.id == db_obj.id


async def test_creates_and_returns_uncommited_model_object_if_autocommit_false(
    db_session_maker,
    db_session: AsyncSession,
    faker: Faker,
    test_repository: TestRepository,
):
    result: TestModel = await test_repository.create(obj_data={"title": faker.pystr()}, autocommit=False)

    async with db_session_maker() as another_session:
        db_obj = await another_session.scalar(select(TestModel))

    assert result.id
    assert not db_obj
