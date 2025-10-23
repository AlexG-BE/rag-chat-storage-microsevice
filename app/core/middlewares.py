from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.core.config import config


def add_middlewares(app: FastAPI) -> FastAPI:
    """
    Wrap FastAPI application, with various of middlewares
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.backend_cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=[str(origin) for origin in config.backend_cors_headers],
    )
    app.add_middleware(SlowAPIMiddleware)

    return app
