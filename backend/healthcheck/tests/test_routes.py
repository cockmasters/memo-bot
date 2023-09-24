import pytest
from fastapi import status
from httpx import AsyncClient
from pytest_lambda import static_fixture

pytestmark = pytest.mark.asyncio


class TestHealthcheck:
    url = static_fixture("/api/healthcheck/")

    async def test_ok(self, url, client: AsyncClient):
        response = await client.get(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
