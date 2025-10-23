from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

Model = TypeVar("Model", bound=Type[DeclarativeBase])
Schema = TypeVar("Schema", bound=BaseModel)
