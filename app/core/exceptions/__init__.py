from httpx import HTTPError
from pydantic import ValidationError

from app.core.exceptions.error_handlers import (
    base_error_handler,
    external_service_error,
    unhandled_error_handler,
    validation_exception_handler,
)
from app.core.exceptions.exceptions import BaseError

exception_handlers = {
    BaseError: base_error_handler,  # type: ignore[dict-item]
    ValidationError: validation_exception_handler,
    HTTPError: external_service_error,
    Exception: unhandled_error_handler,
}
