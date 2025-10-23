from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.core.enums import ApiTagEnum
from app.core.pagination import Page
from app.schemas.chat_message import ChatMessageCreateSchema, ChatMessageDetailSchema, ChatMessageSchema
from app.schemas.chat_session import (
    ChatSessionCreateSchema,
    ChatSessionDetailSchema,
    ChatSessionSchema,
    ChatSessionUpdateSchema,
)
from app.services.chat_message import ChatMessageService
from app.services.chat_session import ChatSessionService

router = APIRouter(
    prefix="/sessions",
    tags=[ApiTagEnum.CHAT_SESSION],
)


@router.post("", response_model=ChatSessionDetailSchema, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: ChatSessionCreateSchema,
    *,
    service: Annotated[ChatSessionService, Depends()],
):
    return await service.create(obj=session_data)


@router.get("/{session_id}", response_model=ChatSessionDetailSchema)
async def get_session(
    session_id: UUID,
    *,
    service: Annotated[ChatSessionService, Depends()],
):
    return await service.get(obj_id=session_id)


@router.get("", response_model=Page[ChatSessionSchema])
async def get_user_sessions(
    user_id: Annotated[UUID, Query()],
    *,
    service: Annotated[ChatSessionService, Depends()],
):
    return await service.get_all_by_user_id(user_id=user_id)


@router.patch("/{session_id}", response_model=ChatSessionDetailSchema)
async def update_session(
    session_id: UUID,
    session_data: ChatSessionUpdateSchema,
    *,
    service: Annotated[ChatSessionService, Depends()],
):
    return await service.update(obj_id=session_id, obj=session_data)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: UUID,
    *,
    service: Annotated[ChatSessionService, Depends()],
):
    return await service.delete(obj_id=session_id)


@router.post("/{session_id}/messages", response_model=ChatMessageDetailSchema, status_code=status.HTTP_201_CREATED)
async def create_session_message(
    session_id: UUID,
    session_data: ChatMessageCreateSchema,
    *,
    service: Annotated[ChatSessionService, Depends()],
    message_service: Annotated[ChatMessageService, Depends()],
):
    await service.get(obj_id=session_id)  # Check if ChatSession exists
    session_data.session_id = session_id

    return await message_service.create(obj=session_data)


@router.get("/{session_id}/messages", response_model=Page[ChatMessageSchema])
async def get_session_messages(
    session_id: UUID,
    *,
    service: Annotated[ChatSessionService, Depends()],
    message_service: Annotated[ChatMessageService, Depends()],
):
    await service.get(obj_id=session_id)  # Check if ChatSession exists
    return await message_service.get_all_by_session_id(session_id=session_id)
