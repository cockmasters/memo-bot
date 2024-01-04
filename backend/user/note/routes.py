from core.postgres import get_session
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from user.dependencies import get_current_user
from user.models import User
from user.note.dependencies import get_current_note
from user.note.models import Note
from user.note.schemas import NoteCreate, NoteFilter, NoteFull, NoteUpdate

user_notes_router = APIRouter()
notes_router = APIRouter()


# TODO : убрать get_current_user, переписать get_current_note
@user_notes_router.post("/", status_code=status.HTTP_201_CREATED, response_model=NoteFull)
async def create(
    note_create: NoteCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await Note.create(user.id, **note_create.model_dump(), session=session)


@notes_router.put("/{note_id}/", response_model=NoteFull)
async def edit(
    update_note: NoteUpdate,
    current_note: Note = Depends(get_current_note),
    session: AsyncSession = Depends(get_session),
):
    return await Note.edit(current_note, update_note, session=session)


@user_notes_router.delete("/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    note: Note = Depends(get_current_note),
    session: AsyncSession = Depends(get_session),
):
    await Note.delete(note.user_id, note.title, session)


@user_notes_router.get("/{title}/", response_model=NoteFull)
async def get_by_title(
    title: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await Note.search_by_title(user.id, title, session)


@user_notes_router.get("/all/", response_model=list[NoteFull])
async def get_all(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await Note.get_all(user.id, session)


@user_notes_router.post("/filter/")
async def filter_by_title_and_tags(
    note: NoteFilter,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await Note.filter(user.id, note, session)
