from typing import Any
from uuid import UUID

from pydantic.json_schema import SkipJsonSchema

from app.core.enums import SenderTypeEnum
from app.core.schemas import BaseSchema


class ChatMessageBaseSchema(BaseSchema):
    id: UUID
    session_id: UUID
    sender: SenderTypeEnum
    content: str
    context: dict[str, Any]


class ChatMessageSchema(ChatMessageBaseSchema): ...


class ChatMessageDetailSchema(ChatMessageBaseSchema): ...


class ChatMessageCreateSchema(BaseSchema):
    session_id: SkipJsonSchema[UUID] = None
    sender: SenderTypeEnum
    content: str
    context: dict[str, Any]
