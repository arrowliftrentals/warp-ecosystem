"""Minimum Viable Atlas (MVA) acceptance tests.

These exist as xfail targets until the relevant build tier is complete.
See Volume 0 Section 12 for the MVA definition.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.acceptance
@pytest.mark.xfail(reason="Tier 2 not yet implemented", strict=False)
async def test_mva_1_basic_conversation(client: AsyncClient) -> None:
    """MVA-1: Send hello, receive coherent response within 5s."""
    response = await client.post(
        "/v1/atlas/chat", json={"query": "hello"}, timeout=5.0
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0


@pytest.mark.acceptance
@pytest.mark.xfail(reason="Tier 4 not yet implemented", strict=False)
async def test_mva_2_evidence_grounded(client: AsyncClient) -> None:
    """MVA-2: Factual question returns evidence-grounded response."""
    response = await client.post(
        "/v1/atlas/chat",
        json={"query": "What memory layers does Atlas have?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    # Evidence grounding: response metadata should include sources
    assert "evidence" in data or "sources" in data


@pytest.mark.acceptance
@pytest.mark.xfail(reason="Tier 3 not yet implemented", strict=False)
async def test_mva_3_memory_round_trip(client: AsyncClient) -> None:
    """MVA-3: Store a fact, retrieve it in a later query."""
    # Store
    await client.post(
        "/v1/atlas/chat",
        json={"query": "My favorite color is blue"},
    )
    # Retrieve
    response = await client.post(
        "/v1/atlas/chat",
        json={"query": "What is my favorite color?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "blue" in data.get("response", "").lower()


@pytest.mark.acceptance
@pytest.mark.xfail(reason="Tier 5 not yet implemented", strict=False)
async def test_mva_4_learning_round_trip(client: AsyncClient) -> None:
    """MVA-4: Correct a classification, verify it persists."""
    # This test will be fleshed out when the learning subsystem is built
    response = await client.post(
        "/v1/atlas/chat",
        json={"query": "correct: that was a memory query, not a search"},
    )
    assert response.status_code == 200


@pytest.mark.acceptance
async def test_mva_5_server_health(client: AsyncClient) -> None:
    """MVA-5: Server boots, /health returns all subsystems healthy."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
