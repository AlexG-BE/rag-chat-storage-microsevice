from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page as FastAPIPaginationPage
from fastapi_pagination.customization import CustomizedPage, UseParamsFields

T = TypeVar("T")

Page = CustomizedPage[
    FastAPIPaginationPage[T],
    UseParamsFields(size=Query(20, ge=1, le=200)),
]
