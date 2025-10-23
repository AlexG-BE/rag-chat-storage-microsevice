from uuid import UUID

from fastapi_pagination.links import Page

from app.core.mixins.service import CRUDServiceMixin
from app.models import ChatMessage
from app.repositories.chat_message import ChatMessageRepository
from app.schemas.chat_message import ChatMessageSchema


class ChatMessageService(CRUDServiceMixin[ChatMessageRepository, ChatMessage, ChatMessageSchema]):
    repository_class = ChatMessageRepository

    async def get_all_by_session_id(
        self,
        session_id: UUID,
        *,
        raw_result: bool = False,
    ) -> Page[ChatMessageSchema] | list[ChatMessage]:
        return await self.repository.get_all_by_session_id(session_id=session_id, raw_result=raw_result)
