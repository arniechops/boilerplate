from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize DB connections, caches, etc.
    yield
    # Shutdown: close connections, flush buffers, etc.


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.include_router(health.router, prefix=settings.api_prefix)

    return app


app = create_app()
