import re
from typing import NoReturn, Type

from sqlalchemy.exc import DBAPIError, NoResultFound

from app.core.enums import PGErrorCodeEnum
from app.core.exceptions import BaseError
from app.core.exceptions.exceptions import (
    ConflictError,
    ForeignKeyError,
    LogicalConstraintViolationError,
    NotFoundError,
    NotNullViolationError,
)

db_error_mapping: dict[PGErrorCodeEnum, Type[BaseError]] = {
    PGErrorCodeEnum.NOT_NULL_VIOLATION: NotNullViolationError,
    PGErrorCodeEnum.CONSTRAINT_VIOLATION: LogicalConstraintViolationError,
    PGErrorCodeEnum.FOREIGN_KEY_VIOLATION: ForeignKeyError,
    PGErrorCodeEnum.UNIQUE_VIOLATION: ConflictError,
}


def extract_field_values_from_pg_error(error_message: str) -> dict[str, str]:
    """
    Extract field names and their values from PostgreSQL error message.

    Examples:
    - "Key (name)=(Test Bank)" -> {"name": "Test Bank"}
    - "Key (name, email)=(John, john@example.com)" -> {"name": "John", "email": "john@example.com"}

    :param error_message: PostgreSQL error message

    :return: Dictionary mapping field names to their values
    """

    if not error_message:
        return {}

    # Pattern to match "Key (field1, field2, ...)=(value1, value2, ...)"
    pattern = r"Key \(([^)]+)\)=\(([^)]+)\)"
    match = re.search(pattern, error_message)

    if not match:
        return {}

    fields_str = match.group(1)
    values_str = match.group(2)

    fields = [field.strip() for field in fields_str.split(",")]
    values = [value.strip() for value in values_str.split(",")]

    if len(fields) != len(values):
        return {}

    return dict(zip(fields, values))


def raise_db_error(ex: DBAPIError) -> NoReturn:
    """
    Raises a more specific database error based on the given DBAPIError exception.

    :param ex: The DBAPIError exception to be handled.

    :raise: A more specific error based on the error mapping,
            or re-raises the original error if the "pgcode" is not found in the mapping.
    """

    if isinstance(ex, NoResultFound):
        raise NotFoundError

    if (error_class := db_error_mapping.get(ex.orig.pgcode)) is not None:
        raise error_class(fields=extract_field_values_from_pg_error(", ".join(ex.orig.args)))

    raise ex
