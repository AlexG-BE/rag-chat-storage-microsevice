from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import SenderTypeEnum
from app.core.models import Base, CommonMixin


class ChatMessage(CommonMixin, Base):
    session_id: Mapped[UUID] = mapped_column(ForeignKey("chat_session.id", ondelete="CASCADE"))
    sender: Mapped[SenderTypeEnum] = mapped_column(ENUM(SenderTypeEnum, name="sender_type_enum"))
    content: Mapped[str]
    context: Mapped[dict[str, Any]] = mapped_column(default=dict, server_default="{}")

    __table_args__ = (Index("ix_chat_message_session_id_created_at", "session_id", "created_at"),)
