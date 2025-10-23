from uuid import UUID

from app.core.mixins.service import CRUDServiceMixin
from app.core.pagination import Page
from app.models import ChatSession
from app.repositories.chat_session import ChatSessionRepository
from app.schemas.chat_session import ChatSessionSchema


class ChatSessionService(CRUDServiceMixin[ChatSessionRepository, ChatSession, ChatSessionSchema]):
    repository_class = ChatSessionRepository

    async def get_all_by_user_id(
        self,
        user_id: UUID,
        *,
        raw_result: bool = False,
    ) -> Page[ChatSessionSchema] | list[ChatSession]:
        return await self.repository.get_all_by_user_id(user_id=user_id, raw_result=raw_result)
