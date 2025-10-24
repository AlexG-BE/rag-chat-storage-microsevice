from fastapi import status
from httpx import AsyncClient


async def test_health_check_success(client: AsyncClient):
    response = await client.get("/api/health-check")

    assert response.status_code == status.HTTP_200_OK
