from datetime import datetime
from typing import Optional

from sqlalchemy.exc import IntegrityError

from core.postgres.base import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, insert, select, UniqueConstraint, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload
from sqlalchemy.testing.schema import Table

from note.exceptions import NoteExists, NoteNotExists
from note.schemas import NoteUpdate

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
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    tags: Mapped[list["Tag"]] = relationship(
        back_populates="notes", secondary=association_table
    )
    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uix_title_user_id"),
    )

    @staticmethod
    async def get_by_user_id(user_id: int, session: AsyncSession) -> "Note":
        query = select(Note).where(Note.user_id == user_id).options(joinedload(Note.tags))
        return (await session.execute(query)).scalars().unique().first()

    @staticmethod
    async def create(
        user_id: int, title: str, body: str, tags: Optional[list[str]], session: AsyncSession
    ) -> "Note":
        note: Note = Note(
            user_id=user_id,
            title=title,
            body=body
        )
        note.tags = [await Tag.create_or_get(user_id, tag, session) for tag in tags] if tags else []
        session.add(note)
        try:
            await session.commit()
        except IntegrityError as e:
            raise NoteExists from e
        return note

    @staticmethod
    async def delete(
        user_id: int, title: str, session: AsyncSession
    ):
        note_id: int = (await Note.search_by_title(user_id, title, session)).id
        association_delete = delete(association_table).filter_by(note_id=note_id).returning(association_table)
        await session.execute(association_delete)
        query = delete(Note).filter_by(user_id=user_id, title=title).returning(Note)
        note = (await session.execute(query)).scalars().first()
        return note

    @staticmethod
    async def edit(
        user_id: int, old_title: str, note: NoteUpdate, session: AsyncSession
    ) -> "Note":
        current_note: "Note" = await Note.search_by_title(user_id, old_title, session)
        note.tags = [await Tag.create_or_get(user_id, tag, session) for tag in note.tags] if note.tags else None
        for key, value in note.model_dump().items():
            setattr(current_note, key, value) if value else None
        return current_note

    @staticmethod
    async def search_by_title(
        user_id: int, title: str, session: AsyncSession
    ) -> "Note":
        query = select(Note).where(Note.user_id == user_id, Note.title == title).options(joinedload(Note.tags))
        note: Optional["Note"] = (await session.execute(query)).scalars().unique().first()
        if not note:
            raise NoteNotExists(title=title)
        return note

    @staticmethod
    async def search_by_tags(
        user_id: int, tags: list[str], session: AsyncSession
    ) -> list["Note"]:
        query = select(Note).where(Note.user_id == user_id).options(joinedload(Note.tags)).order_by(Note.title)
        notes = list((await session.execute(query)).scalars().unique().all())
        notes_by_tags: list["Note"] = []
        for note in notes:
            tags_names: list[str] = [tag.name for tag in note.tags]
            if set(tags).issubset(tags_names):
                notes_by_tags.append(note)
        return notes_by_tags

    @staticmethod
    async def get_all(user_id: int, session: AsyncSession) -> list["Note"]:
        query = select(Note).where(Note.user_id == user_id).options(joinedload(Note.tags)).order_by(Note.title)
        notes = list((await session.execute(query)).scalars().unique().all())
        return notes


class Tag(BaseModel):
    __tablename__ = "tag"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    notes: Mapped[list["Note"]] = relationship(
        back_populates="tags", secondary=association_table
    )

    @staticmethod
    async def create_or_get(user_id: int, name: str, session: AsyncSession) -> "Tag":
        query_select = select(Tag).where(Tag.name == name)
        tag = (await session.execute(query_select)).scalars().first()
        if tag is None:
            query = insert(Tag).values(user_id=user_id, name=name).returning(Tag)
            tag = (await session.execute(query)).scalars().first()
        return tag

    @staticmethod
    async def get_all(user_id: int, session: AsyncSession) -> list["Tag"]:
        query = select(Tag).where(Tag.user_id == user_id)
        tags = list((await session.execute(query)).scalars().all())
        return tags
