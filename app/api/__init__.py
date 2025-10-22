from fastapi import APIRouter, Depends, FastAPI
from fastapi.security import HTTPBearer

from app.api import healthcheck
from app.core.config import config


def add_routes(app: FastAPI, *, prefix=config.base_prefix) -> FastAPI:
    root_router = APIRouter(
        dependencies=[Depends(HTTPBearer(auto_error=False, description="JWT Token"))],
    )

    root_router.include_router(healthcheck.router)

    app.include_router(root_router, prefix=prefix)

    return app
