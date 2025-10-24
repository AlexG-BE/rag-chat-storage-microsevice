import factory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from app.core.mixins.repository import CRUDRepositoryMixin
from app.core.models import Base, CommonMixin
from tests.factories.base import BaseSQLAlchemyFactory


class TestModel(CommonMixin, Base):
    title: Mapped[str]


class TestFactory(BaseSQLAlchemyFactory[TestModel]):
    class Meta:
        model = TestModel

    title: str = factory.Faker("pystr")


class TestRepository(CRUDRepositoryMixin[TestModel, ...]):
    sql_model = TestModel


@pytest.fixture
def test_repository(db_session: AsyncSession) -> TestRepository:
    return TestRepository(db_session)


@pytest.fixture
async def test_object(db_session: AsyncSession) -> TestModel:
    return await TestFactory.provide(db_session).create()
