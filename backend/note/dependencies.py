from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.postgres import get_session
from note.models import Note


async def get_current_note(user_id: int, title: str, session: AsyncSession = Depends(get_session)):
    return await Note.search_by_title(user_id, title, session)
