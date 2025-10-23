from uuid import UUID

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import false

from app.core.models import Base, CommonMixin


class ChatSession(CommonMixin, Base):
    user_id: Mapped[UUID]
    title: Mapped[str]
    is_favorite: Mapped[bool] = mapped_column(default=False, server_default=false())

    __table_args__ = (Index("ix_chat_session_user_id_created_at", "user_id", "created_at"),)
