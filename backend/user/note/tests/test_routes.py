import pytest
from factories import NoteFactory, UserFactory
from httpx import AsyncClient
from pytest_lambda import static_fixture
from sqlalchemy import Exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from user.note.models import Note

pytestmark = pytest.mark.asyncio


class TestCreate:
    url = static_fixture(lambda user_id: f"/api/user/{user_id}/note/")

    async def test_created(self, url, client: AsyncClient, async_session: AsyncSession):
        user = await UserFactory()
        test_param = "string"
        response = await client.post(url(user.id), json={"title": test_param, "body": test_param})
        query = select(Exists(Note)).filter(Note.title == test_param, Note.body == test_param)
        assert response.status_code == status.HTTP_201_CREATED
        assert (await async_session.execute(query)).scalar() is True

    async def test_raises_user_not_exists(self, url, client: AsyncClient):
        response = await client.post(url(727), json={"title": "string", "body": "string"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["code"] == "user_not_exists"


class TestDelete:
    url = static_fixture(lambda user_id, note_id: f"/api/user/{user_id}/note/{note_id}/")

    async def test_deleted(self, url, client: AsyncClient, async_session: AsyncSession):
        user = await UserFactory()
        note = await NoteFactory(user_id=user.id)
        response = await client.delete(url(note.user_id, note.id))
        query = select(Exists(Note)).filter(Note.title == note.title, Note.body == note.body)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not (await async_session.execute(query)).scalar()

    async def test_raises_note_not_exists(self, url, client: AsyncClient):
        user = await UserFactory()
        response = await client.delete(url(user.id, 727))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["code"] == "note_not_exists"


class TestEdit:
    url = static_fixture(lambda note_id: f"/api/note/{note_id}/")

    async def test_edited(self, url, client: AsyncClient, async_session: AsyncSession):
        user = await UserFactory()
        note = await NoteFactory(user_id=user.id)
        test_param = "string"
        await client.put(url(note.id), json={"title": test_param, "body": test_param})
        query = select(Note).where(Note.id == note.id)
        edited_note = (await async_session.execute(query)).scalars().first()
        assert edited_note.title == test_param
        assert edited_note.body == test_param

    async def test_raises_note_not_exists(self, url, client: AsyncClient):
        test_param = "string"
        response = await client.put(url(727), json={"title": test_param, "body": test_param})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["code"] == "note_not_exists"


class TestGetAll:
    url = static_fixture(lambda user_id: f"/api/user/{user_id}/note/all/")

    async def test_get_all(self, url, client: AsyncClient, async_session: AsyncSession):
        num_of_notes = 7
        user = await UserFactory()
        for i in range(num_of_notes):
            await NoteFactory(user_id=user.id)
        response = await client.get(url(user.id))
        assert len(response.json()) == num_of_notes

    async def test_raises_user_not_exists(self, url, client: AsyncClient):
        response = await client.get(url(727))
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["code"] == "user_not_exists"


class TestFilter:
    url = static_fixture(lambda user_id: f"/api/user/{user_id}/note/filter/")

    async def test_filtered_by_title(self, url, client: AsyncClient):
        test_param = "string"
        user = await UserFactory()
        note = await NoteFactory(user_id=user.id, title=test_param)
        await NoteFactory(user_id=user.id, title="not string")
        response = await client.post(url(user.id), json={"title": test_param})
        assert response.json()[0]["id"] == note.id
        assert len(response.json()) == 1
