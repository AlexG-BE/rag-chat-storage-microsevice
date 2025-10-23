from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.mixins.repository import CRUDRepositoryMixin
from app.core.pagination import Page
from app.models import ChatSession
from app.schemas.chat_session import ChatSessionSchema


class ChatSessionRepository(CRUDRepositoryMixin[ChatSession, ChatSessionSchema]):
    sql_model = ChatSession

    async def get_all_by_user_id(
        self,
        user_id: UUID,
        *,
        raw_result: bool = False,
    ) -> Page[ChatSessionSchema] | list[ChatSession]:
        stmt = self.get_query().filter_by(user_id=user_id)

        if raw_result:
            return (await self.session.scalars(stmt)).unique().all()

        return await paginate(self.session, stmt)
