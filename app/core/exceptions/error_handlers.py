from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from httpx import HTTPError, HTTPStatusError
from pydantic import ValidationError

from app.core.config import config
from app.core.exceptions.exceptions import BaseError, ExternalServiceError, InternalServerError
from app.core.logger import log
from app.core.utils import stringify_response


async def base_error_handler(_: Request, exc: BaseError):
    log.error(f"{exc.__class__.__name__}", error=str(exc))

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.content,
    )


async def unhandled_error_handler(request: Request, exc: Exception):
    log.error(f"{exc.__class__.__name__}", error=str(exc))

    return await base_error_handler(request, InternalServerError())


async def validation_exception_handler(_: Request, exc: ValidationError):
    log.error(f"{exc.__class__.__name__}", error=str(exc))

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "title": "Validation error",
            "detail": jsonable_encoder(exc.errors()) if config.internal_env else "Validation error occurred",
        },
    )


async def external_service_error(request: Request, exc: HTTPError):
    """
    Error handler for external service errors.
    For example, when httpx raises an exception due to
    an external service error.
    """

    log.error("External service error", error=exc)

    # If the environment is production / staging, raise a generic error with no details
    if config.external_env:
        return await base_error_handler(request, ExternalServiceError())

    req, res = (exc.request, exc.response) if isinstance(exc, HTTPStatusError) else (None, None)

    default_detail = stringify_response(res) if res else None

    status_code = res.status_code if res else status.HTTP_503_SERVICE_UNAVAILABLE

    content = {
        "title": ExternalServiceError.title,
        "detail": default_detail or ExternalServiceError.default_detail,
    }

    if req:
        content["url"] = str(exc.request.url)

    return JSONResponse(status_code=status_code, content=content)
