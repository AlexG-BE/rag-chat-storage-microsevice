from fastapi import APIRouter, FastAPI

from app.api import chat_session, healthcheck
from app.core.config import config


def add_routes(app: FastAPI, *, prefix=config.base_prefix) -> FastAPI:
    root_router = APIRouter()

    root_router.include_router(healthcheck.router)
    root_router.include_router(chat_session.router)

    app.include_router(root_router, prefix=prefix)

    return app
