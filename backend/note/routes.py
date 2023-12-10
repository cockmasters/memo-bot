from backend.core.postgres import get_session
from backend.user.models import User
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Note, Tag
from .schemas import NoteCreate, NoteFull, TagFull

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NoteFull)
async def create(
    note_create: NoteCreate, user: User, session: AsyncSession = Depends(get_session)
):
    return await Note.create(**note_create, session=session)


@router.get("/all/", response_model=list[NoteFull])
async def get_all(user: User, session: AsyncSession = Depends(get_session)):
    return await Note.get_all(user.id, session)


@router.get("/search/title/", response_model=list[NoteFull])
async def search_by_title(
    title: str, user: User, session: AsyncSession = Depends(get_session)
):
    return await Note.search_by_title(user.id, title, session)


@router.get("/search/tags/", response_model=list[NoteFull])
async def search_by_tags(
    tags: list[str], user: User, session: AsyncSession = Depends(get_session)
):
    return await Note.search_by_tags(user.id, tags, session)


@router.get("/tag/all/", response_model=list[TagFull])
async def get_user_created(user: User, session: AsyncSession = Depends(get_session)):
    return await Tag.get_all(user.id, session)
