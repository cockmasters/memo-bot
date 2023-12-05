import pytest
from backend.user.models import User
from backend.user.tests.factories import UserFactory
from fastapi import status
from httpx import AsyncClient
from pytest_lambda import static_fixture
from sqlalchemy import Exists, select
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


class TestCreate:
    url = static_fixture("/api/user/")

    async def test_ok(self, url: str, client: AsyncClient, async_session: AsyncSession):
        response = await client.post(url, json={"tg_id": 1337, "username": "abobert"})

        query = select(Exists(User)).filter(User.tg_id == 1337)
        assert response.status_code == status.HTTP_201_CREATED
        assert (await async_session.execute(query)).scalar() is True

    async def test_raises_user_exists(self, url: str, client: AsyncClient):
        await UserFactory(tg_id=123)

        response = await client.post(url, json={"tg_id": 123, "username": "abobert"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["code"] == "user_exists"


class TestProfile:
    get_url = static_fixture(lambda tg_id: f"/api/user/{tg_id}/")

    async def test_ok(self, get_url, client: AsyncClient):
        user = await UserFactory(tg_id=123)

        response = await client.get(get_url(123))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["username"] == user.username
