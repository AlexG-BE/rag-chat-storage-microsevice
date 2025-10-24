from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import config

api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key: Annotated[str, Security(api_key_header)]):
    if api_key == config.API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
