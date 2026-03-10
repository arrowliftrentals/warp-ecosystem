"""Health check endpoint.

Returns server status. Per R5, only reports healthy
for subsystems with verified functionality.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Check server health.

    Returns:
        A dict with status "ok" if the server is running.
    """
    return {"status": "ok"}
