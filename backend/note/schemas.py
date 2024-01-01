from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TagCreate(BaseModel):
    user_id: int
    name: str


class TagFull(BaseModel):
    user_id: int
    name: str

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    title: str
    body: str
    tags: Optional[list[str]]


class NoteFull(BaseModel):
    user_id: int
    title: str
    body: str
    created: datetime
    tags: list[TagFull]

    class Config:
        from_attributes = True


class NoteWithoutTags(BaseModel):
    user_id: int
    title: str
    body: str
    created: datetime


class NoteUpdate(BaseModel):
    title: Optional[str]
    body: Optional[str]
    tags: Optional[list[str]]
