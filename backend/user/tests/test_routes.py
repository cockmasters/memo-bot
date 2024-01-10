import pytest
from fastapi import status
from httpx import AsyncClient
from pytest_lambda import static_fixture
from sqlalchemy import Exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from user.models import User
from user.note.models import Note
from user.tests.factories import UserFactory

pytestmark = pytest.mark.asyncio


class TestCreate:
    url = static_fixture("/api/user/")

    async def test_ok(self, url: str, client: AsyncClient, async_session: AsyncSession):
        response = await client.post(url, json={"tg_id": "1337", "vk_id": "1337", "ds_id": "1337"})
        query = select(Exists(User)).filter(User.tg_id == "1337", User.vk_id == "1337", User.ds_id == "1337")
        assert response.status_code == status.HTTP_201_CREATED
        assert (await async_session.execute(query)).scalar() is True

    async def test_raises_user_exists(self, url: str, client: AsyncClient):
        await UserFactory(tg_id="123")

        response = await client.post(url, json={"tg_id": "123"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["code"] == "user_exists"

    async def test_raises_empty_user_socials(self, url: str, client: AsyncClient):
        response = await client.post(url, json={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["code"] == "empty_user_socials"


class TestProfile:
    get_url = static_fixture(lambda tg_id, vk_id, ds_id: f"/api/user/?tg_id={tg_id}&vk_id={vk_id}&ds_id={ds_id}")

    async def test_ok(self, get_url, client: AsyncClient):
        user = await UserFactory(tg_id="123", vk_id="123", ds_id="123")

        response = await client.get(get_url("123", "123", "123"))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == user.id

    async def test_raises_user_not_exists(self, get_url, client: AsyncClient):
        response = await client.get(get_url("727", "727", "727"))

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
        user = await UserFactory(tg_id="123", vk_id="123", ds_id="123")

        response = await client.get(get_url(user.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["code"] is not None

    async def test_raises_user_not_exists(self, get_url, client: AsyncClient):
        response = await client.get(get_url("727"))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["code"] == "user_not_exists"


class TestLinkAccount:
    get_url = static_fixture(lambda user_id: f"/api/user/{user_id}/link/")
    get_url_key = static_fixture(lambda user_id: f"/api/user/{user_id}/auth/key/")

    async def test_ok(self, get_url, get_url_key, client: AsyncClient):
        user_1 = await UserFactory(tg_id=None)
        user_2 = await UserFactory(vk_id=None, ds_id=None)

        response_key = await client.get(get_url_key(user_1.id))
        code = response_key.json()["code"]

        response_linking = await client.post(get_url(user_2.id), json={"code": code})

        assert response_linking.status_code == status.HTTP_204_NO_CONTENT

    async def test_accounts_merged(self, get_url, get_url_key, client: AsyncClient, async_session: AsyncSession):
        tg_id = "11"
        vk_id = "124"
        ds_id = "124"
        user_1 = await UserFactory(tg_id=tg_id, vk_id=None, ds_id=None)
        user_2 = await UserFactory(tg_id=None, vk_id=vk_id, ds_id=ds_id)

        response_key = await client.get(get_url_key(user_1.id))
        code = response_key.json()["code"]
        response_linking = await client.post(get_url(user_2.id), json={"code": code})
        assert response_linking.status_code == status.HTTP_204_NO_CONTENT

        query = select(User)
        merged_user = (await async_session.execute(query)).scalars().first()

        assert merged_user.tg_id == tg_id
        assert merged_user.vk_id == vk_id
        assert merged_user.ds_id == ds_id

    async def test_notes_merged(
        self, get_url, get_url_key, client: AsyncClient, async_session: AsyncSession, note_factory
    ):
        user_1 = await UserFactory(tg_id=None)
        user_2 = await UserFactory(vk_id=None, ds_id=None)
        await note_factory(user_id=user_1.id)
        await note_factory(user_id=user_2.id)

        response_key = await client.get(get_url_key(user_1.id))
        code = response_key.json()["code"]
        response_linking = await client.post(get_url(user_2.id), json={"code": code})

        query = select(User)
        assert response_linking.status_code == status.HTTP_204_NO_CONTENT
        merged_user = (await async_session.execute(query)).scalars().first()
        query_notes = select(Note).where(Note.user_id == merged_user.id)
        notes = (await async_session.execute(query_notes)).scalars().all()
        assert len(notes) == 2

    async def test_raises_user_not_exists(self, get_url, get_url_key, client: AsyncClient):
        user_1 = await UserFactory()

        response_key = await client.get(get_url_key(user_1.id))
        code = response_key.json()["code"]

        response_linking = await client.post(get_url(user_1.id + 1), json={"code": code})

        assert response_linking.status_code == status.HTTP_404_NOT_FOUND
        assert response_linking.json()["code"] == "user_not_exists"

    async def test_raises_code_mismatch(self, get_url, get_url_key, client: AsyncClient):
        user_1 = await UserFactory(vk_id=None, ds_id=None)
        user_2 = await UserFactory(tg_id=None)

        await client.get(get_url_key(user_1.id))

        response_linking = await client.post(get_url(user_2.id), json={"code": "wrong_code"})

        assert response_linking.status_code == status.HTTP_400_BAD_REQUEST
        assert response_linking.json()["code"] == "code_mismatch"
