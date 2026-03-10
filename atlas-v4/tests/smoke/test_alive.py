"""Smoke test: is Atlas alive?

This is the first test that ever runs. If this fails, stop everything.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.smoke
async def test_health_endpoint(client: AsyncClient) -> None:
    """Server boots and /health returns 200 with status ok."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
