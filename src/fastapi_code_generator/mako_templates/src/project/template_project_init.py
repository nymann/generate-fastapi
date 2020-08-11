"""Collection of functions initializing FastAPI application.

This is the main entry point, of creating the FastAPI application. The
application gets created, then gets extensions initialized and routes
registered.
"""

from fastapi import FastAPI

% for model in models:
from ${PROJECT_NAME}.core import version
from ${PROJECT_NAME}.core.db import DB
from ${PROJECT_NAME}.routers import ${model.names.plural_name}_router
% endfor

def create_app() -> FastAPI:
    """Main entry point for creating application

    Returns:
        FastAPI: An instance of fastAPI application.
    """
    app: FastAPI = FastAPI(title="${PROJECT_NAME}", version=version.__version__)
    _initalize_extensions(app=app)
    return _register_routes(app=app)


def _register_routes(app: FastAPI) -> FastAPI:
    """Registers routes on the application

    Args:
        app (FastAPI): FastAPI application

    Returns:
        FastAPI: FastAPI application with routes registered.
    """
    % for model in models:
    app.include_router(${model.names.plural_name}_router.router, tags=["${model.names.plural_name}"], prefix="/${model.names.plural_name}")
    % endfor

    return app


def _initalize_extensions(app: FastAPI):
    """Initializes extensions such as database

    Args:
        app (FastAPI): FastAPI application
    """
    DB.init_app(app=app)
