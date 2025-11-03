"""HTTP utility functions for API requests."""

from typing import Any

import httpx

from app.core.config import settings


async def make_request(
    method: str, endpoint: str, params: dict[str, Any] | None = None, json_data: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Make an HTTP request to the backend API.

    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint path (will be appended to base URL)
        params: Query parameters
        json_data: JSON body for POST requests

    Returns:
        Response data as dictionary

    Raises:
        Exception: If the request fails
    """
    url = f"{settings.API_BASE_URL}{endpoint}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise Exception(f"API request failed with status {e.response.status_code}: {e.response.text}")
    except httpx.TimeoutException:
        raise Exception(f"Request to {url} timed out")
    except httpx.RequestError as e:
        raise Exception(f"Request to {url} failed: {str(e)}")
