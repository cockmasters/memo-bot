from backend.core.postgres import get_session
from backend.note.models import Note, Tag
from backend.note.schemas import NoteCreate, NoteFull, TagFull
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NoteFull)
async def create(note_create: NoteCreate, session: AsyncSession = Depends(get_session)):
    return await Note.create(**note_create.model_dump(), session=session)


@router.get("/all/", response_model=list[NoteFull])
async def get_all(user_id: int, session: AsyncSession = Depends(get_session)):
    return await Note.get_all(user_id, session)


@router.get("/search/title/", response_model=list[NoteFull])
async def search_by_title(
    title: str, user_id: int, session: AsyncSession = Depends(get_session)
):
    return await Note.search_by_title(user_id, title, session)


@router.get("/search/tags/", response_model=list[NoteFull])
async def search_by_tags(
    tags: list[str], user_id: int, session: AsyncSession = Depends(get_session)
):
    return await Note.search_by_tags(user_id, tags, session)


@router.get("/tag/all/", response_model=list[TagFull])
async def get_user_created(user_id: int, session: AsyncSession = Depends(get_session)):
    return await Tag.get_all(user_id, session)
