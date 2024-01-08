from aioredis import Redis
from core.postgres import get_session as postgres_session
from core.redis import get_session as redis_session
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from user.dependencies import get_current_user
from user.models import User
from user.schemas import UserFull, UserSocials

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token", scheme_name="JWT")
router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserFull)
async def create_user(user_create: UserSocials, session: AsyncSession = Depends(postgres_session)):
    return await User.create(user_create.tg_id, user_create.vk_id, user_create.ds_id, session=session)


@router.get("/", response_model=UserFull)
async def get_user_profile(user: UserSocials, session: AsyncSession = Depends(postgres_session)):
    return await User.get_by_social_id(user.tg_id, user.vk_id, user.ds_id, session=session)


@router.get("/auth/key", response_model=int)
async def get_auth_key(user: User = Depends(get_current_user), session: Redis = Depends(redis_session)):
    pass
