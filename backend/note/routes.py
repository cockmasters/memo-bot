from typing import Optional

from core.postgres import get_session
from note.dependencies import get_current_note
from note.models import Note, Tag
from note.schemas import NoteCreate, NoteFull, TagFull, NoteWithoutTags, NoteUpdate
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from user.dependencies import get_current_user
from user.models import User

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NoteFull)
async def create(
    note_create: NoteCreate, user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await Note.create(user.id, **note_create.model_dump(), session=session)


@router.post("/edit", response_model=NoteFull)
async def edit(
    note: NoteUpdate,
    old_note: Note = Depends(get_current_note),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await Note.edit(user.id, old_note.title, note, session=session)


@router.post("/delete", status_code=status.HTTP_200_OK, response_model=NoteWithoutTags)
async def delete(
    note: Note = Depends(get_current_note),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await Note.delete(user.id, note.title, session)


@router.get("/all/", response_model=list[NoteFull])
async def get_all(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await Note.get_all(user.id, session)


@router.get("/search/title/", response_model=NoteFull)
async def search_by_title(
    note: Note = Depends(get_current_note),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await Note.search_by_title(user.id, note.title, session)


@router.post("/search/tags/", response_model=list[NoteFull])
async def search_by_tags(
    tags: list[str],
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await Note.search_by_tags(user.id, tags, session)


@router.get("/tag/all/", response_model=list[TagFull])
async def get_user_created(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await Tag.get_all(user.id, session)
