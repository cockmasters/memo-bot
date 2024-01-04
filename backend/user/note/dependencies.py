from core.postgres import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from user.note.models import Note


async def get_current_note(note_id: int, session: AsyncSession = Depends(get_session)):
    return await Note.get(note_id, session)
