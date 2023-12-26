from datetime import datetime

from pydantic import BaseModel


class NoteCreate(BaseModel):
    user_id: int
    title: str
    body: str


class NoteFull(BaseModel):
    user_id: int
    title: str
    body: str
    created: datetime

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    user_id: int
    name: str


class TagFull(BaseModel):
    user_id: int
    name: str

    class Config:
        from_attributes = True
