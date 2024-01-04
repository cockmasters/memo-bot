from core.postgres import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from user.models import User


async def get_current_user(user_id: int, session: AsyncSession = Depends(get_session)):
    return await User.get_by_id(user_id, session)
