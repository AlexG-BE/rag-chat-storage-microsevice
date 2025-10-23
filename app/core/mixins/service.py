from abc import ABC
from typing import Annotated, Any, Generic, Type, TypeVar
from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db_session
from app.core.exceptions.exceptions import BadRequestError
from app.core.mixins.repository import CRUDRepositoryMixin
from app.core.pagination import Page
from app.core.types import Model, Schema

Repository = TypeVar("Repository", bound=CRUDRepositoryMixin)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUDServiceMixin(ABC, Generic[Repository, Model, Schema]):
    repository_class: Type[Repository]

    def __init__(self, db_session: Annotated[AsyncSession, Depends(get_db_session)]):
        self.repository: Repository = self.repository_class(db_session)

    async def get(self, obj_id: int | UUID, *, raise_error: bool = True, **kwargs: Any) -> Model | None:
        """
        Get object by id.

        :param obj_id: Object ID.
        :param raise_error: If True, raises an error if the object is not found.
        :param kwargs: Additional keyword arguments.

        :return: SQLAlchemy model.
        """
        return await self.repository.get(obj_id, raise_error=raise_error, **kwargs)

    async def get_all(self, **kwargs: Any) -> Page[Schema] | list[Model]:
        """
        Get all objects.

        :param kwargs: Additional keyword arguments.

        :return: Paginated result.
        """
        return await self.repository.get_all(**kwargs)

    async def create(
        self,
        obj: CreateSchema,
        *,
        autocommit: bool = True,
        **kwargs: Any,
    ) -> Model:
        """
        Creates an entity in the database, and returns the created object.

        :param obj: Pydantic model.
        :param autocommit: If True, commits changes to a database, if False - flushes them.
        :param kwargs: Additional keyword arguments.

        :return: Created entity.
        """
        return await self.repository.create(obj.model_dump(), autocommit=autocommit, **kwargs)

    async def update(self, obj_id: int | UUID, obj: UpdateSchema, *, autocommit: bool = True, **kwargs: Any) -> Model:
        """
        Updates an entity in the database, and returns the updated object.

        :param obj_id: Object ID.
        :param obj: Object to update.
        :param autocommit: If True, commits changes to a database, if False - flushes them.
        :param kwargs: Additional keyword arguments.

        :return: Updated entity.
        """
        if not (obj_data := obj.model_dump(exclude_unset=True)):
            raise BadRequestError("No data provided for updating")

        return await self.repository.update(obj_id, obj_data, autocommit=autocommit, **kwargs)

    async def delete(self, obj_id: int | UUID, *, autocommit: bool = True, **kwargs: Any) -> None:
        """
        Deletes an entity from the database.

        :param obj_id: Object ID.
        :param autocommit: If True, commits changes to a database, if False - flushes them.
        :param kwargs: Additional keyword arguments.

        :return: None.
        """
        return await self.repository.delete(obj_id, autocommit=autocommit, **kwargs)
