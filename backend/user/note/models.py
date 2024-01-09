import asyncio
from datetime import datetime
from typing import Optional

from core.postgres.base import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from sqlalchemy.testing.schema import Table
from user.note.exceptions import NoteExists, NoteNotExists
from user.note.schemas import NoteFilter, NoteUpdate

association_table = Table(
    "notes_tags",
    BaseModel.metadata,
    Column("note_id", ForeignKey("note.id", ondelete="cascade"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="cascade"), primary_key=True),
)


class Note(BaseModel):
    __tablename__ = "note"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="cascade"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    tags: Mapped[list["Tag"]] = relationship(back_populates="notes", secondary=association_table)

    @staticmethod
    async def get_by_user_id(user_id: int, session: AsyncSession) -> "Note":
        query = select(Note).where(Note.user_id == user_id).options(joinedload(Note.tags))
        return (await session.execute(query)).scalars().unique().first()

    @staticmethod
    async def create(
        user_id: int,
        title: str,
        body: str,
        tags: Optional[list[str]],
        session: AsyncSession,
    ) -> "Note":
        note: Note = Note(user_id=user_id, title=title, body=body)
        note.tags = [await Tag.create_or_get(tag, session) for tag in tags] if tags else []
        session.add(note)
        try:
            await session.commit()
        except IntegrityError as e:
            raise NoteExists(title=title) from e
        return note

    @staticmethod
    async def delete(note_id: int, session: AsyncSession):
        association_delete = delete(association_table).filter_by(note_id=note_id).returning(association_table)
        await session.execute(association_delete)
        query = delete(Note).filter_by(id=note_id)
        await session.execute(query)

    @staticmethod
    async def edit(current_note: "Note", update_note: NoteUpdate, session: AsyncSession) -> "Note":
        if update_note.tags is not None:
            coroutines = [Tag.create_or_get(tag, session) for tag in update_note.tags]
            update_note.tags = await asyncio.gather(*coroutines)
        for key, value in update_note.model_dump().items():
            setattr(current_note, key, value) if value is not None else None
        try:
            await session.commit()
        except IntegrityError as e:
            raise NoteExists(title=update_note.title) from e
        return current_note

    @staticmethod
    async def search_by_title(user_id: int, title: str, session: AsyncSession) -> "Note":
        query = select(Note).where(Note.user_id == user_id, Note.title == title).options(joinedload(Note.tags))
        note: Optional["Note"] = (await session.execute(query)).scalars().unique().first()
        return note

    @staticmethod
    async def filter(user_id: int, note: NoteFilter, session: AsyncSession) -> list["Note"]:
        query = select(Note).where(Note.user_id == user_id).options(joinedload(Note.tags)).order_by(Note.title)
        if note.title is not None:
            query = query.where(Note.title == note.title)
        if note.tags:
            query = (
                query.join(Note.tags)
                .filter(Tag.name.in_(note.tags))
                .group_by(Note.id)
                .having(func.count(Note.id) == len(note.tags))
            )
        return list((await session.execute(query)).scalars().unique().all())

    @staticmethod
    async def get(note_id: int, session: AsyncSession) -> "Note":
        query = select(Note).where(Note.id == note_id).options(joinedload(Note.tags))
        note: Note = (await session.execute(query)).scalars().unique().first()
        if not note:
            raise NoteNotExists
        return note

    @staticmethod
    async def get_all(user_id: int, session: AsyncSession) -> list["Note"]:
        query = select(Note).where(Note.user_id == user_id).options(joinedload(Note.tags)).order_by(Note.title)
        notes = list((await session.execute(query)).scalars().unique().all())
        return notes

    @staticmethod
    async def replace_author(old_user_id: int, new_user_id: int, session: AsyncSession):
        query = update(Note).where(Note.user_id == old_user_id).values(user_id=new_user_id)
        await session.execute(query)


class Tag(BaseModel):
    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    notes: Mapped[list["Note"]] = relationship(back_populates="tags", secondary=association_table)

    @staticmethod
    async def create_or_get(name: str, session: AsyncSession) -> "Tag":
        query_select = select(Tag).where(Tag.name == name)
        tag = (await session.execute(query_select)).scalars().first()
        if tag is None:
            query = insert(Tag).values(name=name).returning(Tag)
            tag = (await session.execute(query)).scalars().first()
        return tag

    @staticmethod
    async def get_all(session: AsyncSession) -> list["Tag"]:
        query = select(Tag)
        tags = list((await session.execute(query)).scalars().all())
        return tags
