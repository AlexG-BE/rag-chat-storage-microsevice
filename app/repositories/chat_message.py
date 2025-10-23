from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate

from app.core.mixins.repository import CRUDRepositoryMixin
from app.core.pagination import Page
from app.models import ChatMessage
from app.schemas.chat_message import ChatMessageSchema


class ChatMessageRepository(CRUDRepositoryMixin[ChatMessage, ChatMessageSchema]):
    sql_model = ChatMessage

    async def get_all_by_session_id(
        self,
        session_id: UUID,
        *,
        raw_result: bool = False,
    ) -> Page[ChatMessageSchema] | list[ChatMessage]:
        stmt = self.get_query().filter_by(session_id=session_id)

        if raw_result:
            return (await self.session.scalars(stmt)).unique().all()

        return await paginate(self.session, stmt)
