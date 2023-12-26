from datetime import datetime

from sqlalchemy.exc import IntegrityError

from core.postgres.base import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, insert, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.testing.schema import Table

from note.exceptions import NoteExists

association_table = Table(
    "notes_tags",
    BaseModel.metadata,
    Column("note_id", ForeignKey("note.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Note(BaseModel):
    __tablename__ = "note"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    tags: Mapped[list["Tag"]] = relationship(
        back_populates="notes", secondary=association_table
    )

    @staticmethod
    async def get_by_user_id(user_id: int, session: AsyncSession) -> "Note":
        query = select(Note).where(Note.user_id == user_id)
        return (await session.execute(query)).scalars().first()

    @staticmethod
    async def create(
        user_id: int, title: str, body: str, session: AsyncSession
    ) -> "Note":
        query = (
            insert(Note).values(user_id=user_id, title=title, body=body).returning(Note)
        )
        try:
            note = (await session.execute(query)).scalars().first()
        except IntegrityError as e:
            raise NoteExists(title=title) from e
        return note

    @staticmethod
    async def search_by_title(
        user_id: int, title: str, session: AsyncSession
    ) -> list["Note"]:
        query = select(Note).where(Note.user_id == user_id, Note.title == title)
        notes: list = list((await session.execute(query)).scalars().all())
        return notes

    @staticmethod
    async def search_by_tags(
        user_id: int, tags: list[str], session: AsyncSession
    ) -> list["Note"]:
        pass

    @staticmethod
    async def get_all(user_id: int, session: AsyncSession) -> list["Note"]:
        query = select(Note).where(Note.user_id == user_id)
        notes = list((await session.execute(query)).scalars().all())
        return notes


class Tag(BaseModel):
    __tablename__ = "tag"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    notes: Mapped[list["Note"]] = relationship(
        back_populates="tags", secondary=association_table
    )

    @staticmethod
    async def create_or_update(user_id: int, name: str, session: AsyncSession) -> "Tag":
        query = (
            pg_insert(Tag)
            .values(user_id=user_id, name=name)
            .on_conflict_do_nothing()
            .returning(Tag)
        )
        tag = (await session.execute(query)).scalars().first()
        return tag

    @staticmethod
    async def get_all(user_id: int, session: AsyncSession) -> list["Tag"]:
        query = select(Tag).where(Tag.user_id == user_id)
        tags = list((await session.execute(query)).scalars().all())
        return tags
