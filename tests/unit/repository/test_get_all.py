from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.fixtures import TestFactory, TestModel, TestRepository


async def test_returns_model_objects_if_raw_result(
    db_session: AsyncSession,
    test_repository: TestRepository,
):
    size = 3
    objects = await TestFactory.provide(db_session).create_batch(size=size)

    result: list[TestModel] = await test_repository.get_all(raw_result=True)

    assert len(result) == size
    assert {i.id for i in result} == {i.id for i in objects}


async def test_returns_empty_list_if_objects_not_exist_and_raw_result(test_repository: TestRepository):
    result: list[TestModel] = await test_repository.get_all(raw_result=True)
    assert not result
