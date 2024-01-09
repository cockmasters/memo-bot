import random
from typing import Optional

from core.postgres import get_session as get_postgres_session
from core.redis import get_session as get_redis_session
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from user.dependencies import get_current_user
from user.exceptions import CodeMismatch
from user.models import User
from user.one_time_code_repository import auth_key_repository
from user.schemas import UserCode, UserFull, UserSocials
from user.services import merge_accounts

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token", scheme_name="JWT")
router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserFull)
async def create(user_create: UserSocials, session: AsyncSession = Depends(get_postgres_session)):
    return await User.create(tg_id=user_create.tg_id, vk_id=user_create.vk_id, ds_id=user_create.ds_id, session=session)


@router.get("/", response_model=UserFull)
async def get_by_social_id(user: UserSocials = Depends(), session: AsyncSession = Depends(get_postgres_session)):
    return await User.get_by_social_id(user.tg_id, user.vk_id, user.ds_id, session=session)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_postgres_session)):
    await User.delete(user.id, session)


@router.get("/{user_id}/auth/key/", response_model=UserCode)
async def get_auth_key(user: User = Depends(get_current_user), session: aioredis.Redis = Depends(get_redis_session)):
    code_list = [str(random.randint(0, 9)) for i in range(6)]
    code = "".join(code_list)
    await auth_key_repository.set(str(user.id), code, session=session)
    return UserCode(code=code)


@router.post("/{user_id}/link/", status_code=status.HTTP_204_NO_CONTENT)
async def link_account(
    code: UserCode,
    user: User = Depends(get_current_user),
    redis_session: aioredis.Redis = Depends(get_redis_session),
    postgres_session: AsyncSession = Depends(get_postgres_session),
):
    user_id: Optional[int] = await auth_key_repository.get_user_id(code.code, redis_session)
    if not user_id:
        raise CodeMismatch
    await merge_accounts(user.id, user_id, postgres_session)
    await auth_key_repository.delete(code, session=redis_session)
