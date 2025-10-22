from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DOUBLE_PRECISION, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, NUMRANGE, Range
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.core.utils import pascal_to_snake


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        UUID: PGUUID,
        float: DOUBLE_PRECISION,
        list[float]: ARRAY(DOUBLE_PRECISION),
        list[int]: ARRAY(Integer),
        list[str]: ARRAY(String),
        dict[str, Any]: JSONB(none_as_null=True),
        list[dict[str, Any]]: JSONB(none_as_null=True),
        Range[float]: NUMRANGE,
    }


class CommonMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
    )

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return pascal_to_snake(cls.__name__)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"
