"""Smoke test fixtures — boots the real Atlas app."""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from atlas.api.server import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Provide an async HTTP client connected to the Atlas app.

    Yields:
        An httpx.AsyncClient that sends requests to the live app.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
