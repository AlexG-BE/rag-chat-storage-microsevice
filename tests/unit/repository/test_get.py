import pytest
from faker import Faker

from app.core.exceptions.exceptions import NotFoundError
from tests.unit.fixtures import TestModel, TestRepository


async def test_returns_model_object(
    test_repository: TestRepository,
    test_object: TestModel,
):
    result: TestModel = await test_repository.get(obj_id=test_object.id)

    assert result.id == test_object.id


async def test_returns_not_found_error_if_object_not_exists(
    faker: Faker,
    test_repository: TestRepository,
):
    with pytest.raises(NotFoundError):
        await test_repository.get(obj_id=faker.uuid4(cast_to=None))


async def test_returns_none_if_object_not_exists_and_raise_error_false(
    faker: Faker,
    test_repository: TestRepository,
):
    result = await test_repository.get(obj_id=faker.uuid4(cast_to=None), raise_error=False)
    assert not result
