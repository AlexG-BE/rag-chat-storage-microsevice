import json
from typing import Any

from fastapi import status

# mypy: disable-error-code="dict-item"


class BaseError(Exception):
    """
    Base error class
    """

    title: str
    default_detail: str
    content: dict
    status_code: int

    def __init__(self, detail: str | None = None, fields: dict[str, str] | None = None, **kwargs: Any) -> None:
        formatted_fields = ", ".join(f"{field}={value}" for field, value in (fields or {}).items())

        errors = [
            detail or self.default_detail,
            f"Fields: {formatted_fields}" if formatted_fields else None,
        ]

        self.content = {
            "title": self.title,
            "detail": ". ".join(filter(None, errors)),
            **kwargs,
        }

    def __str__(self) -> str:
        return json.dumps(self.content)


class BadRequestError(BaseError):
    """
    The server cannot or will not process the request due to an apparent client error
    """

    title = "Bad Request"
    default_detail = "The server cannot process the request from the client"
    status_code = status.HTTP_400_BAD_REQUEST


class TooManyRequestsError(BadRequestError):
    """
    The server cannot or will not process the request due to an apparent client error
    """

    title = "Too Many Requests"
    default_detail = "The server cannot process the request from the client"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class ForbiddenError(BaseError):
    """
    The client does not have access rights to the content
    """

    title = "Forbidden"
    default_detail = "Forbidden"
    status_code = status.HTTP_403_FORBIDDEN


class UnauthorizedError(BaseError):
    """
    The client must authenticate itself to get the requested response
    """

    title = "Unauthorized"
    default_detail = "Unauthorized"
    status_code = status.HTTP_401_UNAUTHORIZED


class UnprocessableEntityError(BaseError):
    """
    The request was well-formed but was unable to be followed due to semantic errors
    """

    title = "Unprocessable Entity"
    default_detail = "Unprocessable Entity"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class NotFoundError(BaseError):
    """
    The server can not find the requested resource
    """

    title = "Not Found"
    default_detail = "Not Found"
    status_code = status.HTTP_404_NOT_FOUND


class RequestTimeoutError(BaseError):
    """
    The server would like to shut down this unused connection
    """

    title = "Request Timeout"
    default_detail = "Request Timeout"
    status_code = status.HTTP_408_REQUEST_TIMEOUT


class ConflictError(BaseError):
    """
    The request could not be completed due to a conflict with the current state of the resource
    """

    title = "Conflict"
    default_detail = "Duplicate entries found"
    status_code = status.HTTP_409_CONFLICT


class InternalServerError(BaseError):
    """
    The request could not be completed due to a server issue
    """

    title = "Internal Server Error"
    default_detail = "Something went wrong on the server. Please try again later"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ForeignKeyError(UnprocessableEntityError):
    """
    The request couldn't be completed due to a ForeignKey error
    """

    default_detail = "Related entity conflict"


class DuplicatesError(BadRequestError):
    """
    The request couldn't be completed due to a DuplicatesError error
    """

    default_detail = "Duplicate error"


class NotNullViolationError(UnprocessableEntityError):
    """
    The request couldn't be completed due to a NotNullViolationError error
    """

    default_detail = "Required field is missing"


class LogicalConstraintViolationError(UnprocessableEntityError):
    """
    The request couldn't be completed due to a LogicalConstraintViolationError error
    """

    default_detail = "Logical constraint violation"


class ExternalServiceError(BaseError):
    """
    Error raised when an external service returns an error
    """

    title = "External Service Error"
    default_detail = "An error occurred while processing the request with an external service"
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
