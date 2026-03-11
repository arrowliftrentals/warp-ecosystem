"""Atlas v4 FastAPI server.

Minimal server with /health endpoint. This is the Tier 1 skeleton
that acceptance test fixtures boot.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from atlas.api.routes.health import router as health_router
from atlas.shared.config import get_config
from atlas.shared.logging import setup_logging


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Initialize Atlas on server startup."""
    config = get_config()
    setup_logging(config.log_level)
    yield


app = FastAPI(
    title="Atlas v4",
    description="Autonomous Technological Learning Adaptive System",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
