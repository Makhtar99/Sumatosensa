import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio  
async def test_root_endpoint(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200