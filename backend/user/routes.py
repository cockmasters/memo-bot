from core.postgres import get_session
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate, UserFull

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token", scheme_name="JWT")

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserFull)
async def create_user(
    user_create: UserCreate, session: AsyncSession = Depends(get_session)
):
    return await User.create(
        tg_id=user_create.tg_id, username=user_create.username, session=session
    )


@router.get("/{tg_id}/", response_model=UserFull)
async def get_user_profile(tg_id: int, session: AsyncSession = Depends(get_session)):
    return await User.get_by_id(tg_id, session=session)
