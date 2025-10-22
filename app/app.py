from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from app.api import add_routes
from app.core.config import config
from app.core.exceptions import exception_handlers

disable_installed_extensions_check()


def create_app() -> FastAPI:
    app_instance = FastAPI(
        openapi_url=config.openapi_url,
        redoc_url=config.redoc_url,
        docs_url=config.swagger_url,
        exception_handlers=exception_handlers,
    )

    add_routes(app_instance)
    add_pagination(app_instance)

    @app_instance.get(config.base_prefix, include_in_schema=False)
    @app_instance.get("", include_in_schema=False)
    async def root():
        return RedirectResponse(url=config.swagger_url)

    return app_instance


app = create_app()
