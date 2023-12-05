from backend.core.postgres.base import BaseModel
from backend.user.exceptions import UserExists
from sqlalchemy import Column, Integer, String, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped


class User(BaseModel):
    __tablename__ = "user"

    tg_id: Mapped[int] = Column(Integer, unique=True, index=True, nullable=False)
    username: Mapped[str] = Column(String, unique=True, nullable=False)

    @staticmethod
    async def get_by_id(tg_id: int, session: AsyncSession) -> "User":
        query = select(User).where(User.tg_id == tg_id)
        return (await session.execute(query)).scalars().first()

    @staticmethod
    async def create(tg_id: int, username: str, session: AsyncSession) -> "User":
        query = insert(User).values(tg_id=tg_id, username=username).returning(User)
        try:
            user = (await session.execute(query)).scalars().first()
        except IntegrityError as e:
            raise UserExists(username=username) from e
        return user
