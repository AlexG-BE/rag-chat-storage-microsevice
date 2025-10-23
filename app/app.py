from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api import add_routes
from app.core.config import config
from app.core.exceptions import exception_handlers
from app.core.middlewares import add_middlewares

disable_installed_extensions_check()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[config.limiter_limit],
    enabled=bool(config.limiter_limit),
)


def create_app() -> FastAPI:
    app_instance = FastAPI(
        openapi_url=config.openapi_url,
        redoc_url=config.redoc_url,
        docs_url=config.swagger_url,
        exception_handlers=exception_handlers,
    )

    app_instance.state.limiter = limiter

    add_middlewares(app_instance)
    add_routes(app_instance)
    add_pagination(app_instance)

    @app_instance.get(config.base_prefix, include_in_schema=False)
    @app_instance.get("", include_in_schema=False)
    async def root():
        return RedirectResponse(url=config.swagger_url)

    return app_instance


app = create_app()
