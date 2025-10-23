from uuid import UUID

from app.core.schemas import BaseSchema


class ChatSessionBaseSchema(BaseSchema):
    id: UUID
    user_id: UUID
    title: str
    is_favorite: bool


class ChatSessionSchema(ChatSessionBaseSchema): ...


class ChatSessionDetailSchema(ChatSessionBaseSchema): ...


class ChatSessionCreateSchema(BaseSchema):
    user_id: UUID
    title: str


class ChatSessionUpdateSchema(BaseSchema):
    title: str = None
    is_favorite: bool = None
