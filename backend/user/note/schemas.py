from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class TagCreate(BaseModel):
    name: str


class TagFull(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    title: str
    body: str
    tags: Optional[list[str]] = None


class NoteFull(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    created: datetime
    tags: list

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def string_list_tags(self):
        self.tags = [tag.name for tag in self.tags]
        return self


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[list[str]] = None


class NoteFilter(BaseModel):
    title: Optional[str] = None
    tags: Optional[list[str]] = None
