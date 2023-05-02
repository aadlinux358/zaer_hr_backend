"""Health check tests module."""
import pytest
from fastapi import status
from httpx import URL, AsyncClient


@pytest.mark.asyncio
async def test_hr_service_health_status(client: AsyncClient):
    """Test endpoint works."""
    client.base_url = URL("http://tests")
    response = await client.get("/")
    response_object = response.json()
    assert response.status_code == status.HTTP_200_OK, response_object
    assert response_object["name"] == "hr"
    assert response_object["version"] == "0.1.0"
    assert response_object["description"] == "hr endpoint service"
