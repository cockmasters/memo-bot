from typing import Optional

from core.postgres.base import BaseModel
from sqlalchemy import Integer, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from user.exceptions import UserExists, UserNotExists


class User(BaseModel):
    __tablename__ = "user"

    tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=True)
    vk_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=True)
    ds_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=True)

    @staticmethod
    async def get_by_social_id(tg_id: int, vk_id: int, ds_id: int, session: AsyncSession) -> "User":
        query = select(User).where(User.tg_id == tg_id, User.vk_id == vk_id, User.ds_id == ds_id)
        user: Optional[User] = (await session.execute(query)).scalars().first()
        if not user:
            raise UserNotExists
        return user

    @staticmethod
    async def get_by_id(user_id: int, session: AsyncSession) -> "User":
        query = select(User).where(User.id == user_id)
        user: Optional[User] = (await session.execute(query)).scalars().first()
        if not user:
            raise UserNotExists
        return user

    @staticmethod
    async def create(
        session: AsyncSession, tg_id: Optional[int] = None, vk_id: Optional[int] = None, ds_id: Optional[int] = None
    ) -> "User":
        query = insert(User).values(tg_id=tg_id, vk_id=vk_id, ds_id=ds_id).returning(User)
        try:
            user = (await session.execute(query)).scalars().first()
        except IntegrityError as e:
            raise UserExists from e
        return user

    @staticmethod
    async def delete(user_id: int, session: AsyncSession):
        await session.delete(await User.get_by_id(user_id, session))
