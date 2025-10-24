from asyncio import current_task

import factory
from factory import base
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.core.dependencies.db import get_session_maker
from tests.factories.base.sqlalchemy import AsyncSQLAlchemyFactory

AsyncScopedSession = async_scoped_session(
    session_factory=get_session_maker(),
    scopefunc=current_task,
)


class BaseSQLAlchemyFactory(AsyncSQLAlchemyFactory[base.T]):
    class Meta:
        sqlalchemy_session = AsyncScopedSession
        sqlalchemy_session_persistence = factory.alchemy.SESSION_PERSISTENCE_COMMIT

    @classmethod
    def provide(cls, session: AsyncSession) -> type["BaseSQLAlchemyFactory"]:
        cls._meta.sqlalchemy_session = session
        return cls
