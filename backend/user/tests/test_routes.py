import pytest
from fastapi import status
from httpx import AsyncClient
from pytest_lambda import static_fixture
from sqlalchemy import Exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from user.models import User
from user.tests.factories import UserFactory

pytestmark = pytest.mark.asyncio


class TestCreate:
    url = static_fixture("/api/user/")

    async def test_ok(self, url: str, client: AsyncClient, async_session: AsyncSession):
        response = await client.post(url, json={"tg_id": 1337, "vk_id": 1337, "ds_id": 1337})
        query = select(Exists(User)).filter(User.tg_id == 1337)
        assert response.status_code == status.HTTP_201_CREATED
        assert (await async_session.execute(query)).scalar() is True

    async def test_raises_user_exists(self, url: str, client: AsyncClient):
        await UserFactory(tg_id=123)

        response = await client.post(url, json={"tg_id": 123})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["code"] == "user_exists"

    async def test_raises_empty_user_socials(self, url: str, client: AsyncClient):
        response = await client.post(url, json={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["code"] == "empty_user_socials"


class TestProfile:
    get_url = static_fixture(lambda tg_id, vk_id, ds_id: f"/api/user/?tg_id={tg_id}&vk_id={vk_id}&ds_id={ds_id}")

    async def test_ok(self, get_url, client: AsyncClient):
        user = await UserFactory(tg_id=123, vk_id=123, ds_id=123)

        response = await client.get(get_url(123, 123, 123))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == user.id

    async def test_raises_user_not_exists(self, get_url, client: AsyncClient):
        response = await client.get(get_url(727, 727, 727))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["code"] == "user_not_exists"

    async def test_raises_empty_user_socials(self, client: AsyncClient):
        url = "/api/user/"
        response = await client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["code"] == "empty_user_socials"


class TestAuthKey:
    get_url = static_fixture(lambda user_id: f"/api/user/{user_id}/auth/key/")

    async def test_ok(self, get_url, client: AsyncClient):
        user = await UserFactory(tg_id=123, vk_id=123, ds_id=123)

        response = await client.get(get_url(user.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["code"] is not None

    async def test_raise_user_not_exists(self, get_url, client: AsyncClient):
        response = await client.get(get_url(727))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["code"] == "user_not_exists"


class TestLinkAccount:
    get_url = static_fixture(lambda user_id, code: f"/api/user/link/?{code}&{user_id}")

    async def test_ok(self):
        pass
