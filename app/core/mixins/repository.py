from abc import ABC
from typing import Any, Generic, Type
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import Select, delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions.exceptions import NotFoundError
from app.core.helpers.db import raise_db_error
from app.core.pagination import Page
from app.core.types import Model, Schema


class CRUDRepositoryMixin(ABC, Generic[Model, Schema]):
    """
    Base repository class for CRUD operations.
    """

    sql_model: Type[Model]

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_query(self) -> Select:
        """
        Returns a query object for the model.

        :return: Query object.
        """
        return select(self.sql_model)

    async def get_all(self, raw_result: bool = False, **kwargs: Any) -> Page[Schema] | list[Model]:  # type: ignore
        """
        This method retrieves all objects from the database.

        :param raw_result: A flag that determines whether to return a list of raw results without pagination.
                           If True, a list of raw results will be returned.
                           If False, a Page object with paginated results will be returned. Default is False.
        :param kwargs: Additional keyword arguments.

        :return: A Page object with paginated results if raw_result is False, otherwise a list of raw results.

        :raises NoResultFound: If no objects are found in the database.
        """
        stmt = self.get_query()

        if raw_result:
            return (await self.session.scalars(stmt)).unique().all()

        return await paginate(self.session, stmt)

    async def get(self, obj_id: int | UUID, *, raise_error: bool = True, **kwargs: Any) -> Model | None:
        """
        This method retrieves an object from the database using its ID.

        :param obj_id: The ID of the object to be retrieved.
        :param raise_error: A flag that determines whether an error should be raised if the object is not found.
                            If True, a NotFoundError will be raised when the object is not found.
                            If False, the method will return None when the object is not found. Default is True.
        :param kwargs: Additional keyword arguments.

        :return: The retrieved object if it exists. If the object does not exist and raise_error is False, the method
                 will return None.

        :raises NotFoundError: If raise_error is True and the object is not found in the database.
        """
        stmt = self.get_query().filter_by(id=obj_id)

        if not (result := await self.session.scalar(stmt)) and raise_error:
            raise NotFoundError(detail=f"{self.sql_model.__name__} object with {obj_id=!s} not found.")

        return result

    async def _apply_changes(
        self,
        stmt,
        obj_id: int | UUID | None = None,
        *,
        is_unique: bool = True,
        autocommit: bool = False,
    ) -> Model:
        """Internal method to store changes in DB."""
        try:
            result = await self.session.execute(stmt)

            if is_unique:
                result = result.unique()

            result = result.scalar_one()

            if autocommit:
                await self.session.commit()
            else:
                await self.session.flush()

            await self.session.refresh(result)

        except DBAPIError as ex:
            await self.session.rollback()
            raise_db_error(ex)

        except NoResultFound:
            raise NotFoundError(detail=f"{self.sql_model.__name__} object with obj_id={obj_id!s} not found")

        return result

    async def create(
        self,
        obj_data: dict,
        *,
        autocommit: bool = True,
        is_unique: bool = True,
        **kwargs: Any,
    ) -> Model:
        """
        Creates an entity in the database and returns the created object.

        :param obj_data: The object to create.
        :param autocommit: If True, commit changes immediately, otherwise flush changes.
        :param is_unique: If True, apply unique filtering to the objects, otherwise do nothing.
        :param kwargs: Additional keyword arguments.

        :return: The created object.
        """

        stmt = insert(self.sql_model).values(**obj_data).returning(self.sql_model)

        return await self._apply_changes(stmt=stmt, autocommit=autocommit, is_unique=is_unique)

    async def update(
        self,
        obj_id: int | UUID,
        obj_data: dict,
        *,
        autocommit: bool = True,
        is_unique: bool = True,
        **kwargs: Any,
    ) -> Model:
        """
        Updates an object.

        :param obj_id: The ID of the object to update.
        :param obj_data: The object data to update.
        :param autocommit: If True, commit changes immediately, otherwise flush changes.
        :param is_unique: If True, apply unique filtering to the objects, otherwise do nothing.
        :param kwargs: Additional keyword arguments.

        :returns: The updated object.
        """

        stmt = update(self.sql_model).filter_by(id=obj_id).values(**obj_data).returning(self.sql_model)

        return await self._apply_changes(stmt=stmt, obj_id=obj_id, autocommit=autocommit, is_unique=is_unique)

    async def delete(self, obj_id: int | UUID, *, autocommit: bool = True, **kwargs: Any) -> None:
        """
        Delete an object.

        :param obj_id: The ID of the object to delete.
        :param autocommit: If True, commit changes immediately, otherwise flush changes.
        :param kwargs: Additional keyword arguments.

        :raises DBAPIError: If there is an error during database operations.
        :raises NotFoundError: If item does not exist in database.
        """
        await self.get(obj_id=obj_id)

        stmt = delete(self.sql_model).filter_by(id=obj_id)

        try:
            await self.session.execute(stmt)

            if autocommit:
                await self.session.commit()
            else:
                await self.session.flush()

        except DBAPIError as ex:
            await self.session.rollback()
            raise_db_error(ex)
