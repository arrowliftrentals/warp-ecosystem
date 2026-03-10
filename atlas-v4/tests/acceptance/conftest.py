"""Acceptance test fixtures — same as smoke but longer timeout."""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from atlas.api.server import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Provide an async HTTP client for acceptance tests.

    Yields:
        An httpx.AsyncClient connected to the live app.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test", timeout=30.0
    ) as ac:
        yield ac
