from fastapi import status
from httpx import AsyncClient


async def test_health_check_success(client: AsyncClient, api_key_headers: dict):
    response = await client.get("/api/health-check", headers=api_key_headers)

    assert response.status_code == status.HTTP_200_OK
