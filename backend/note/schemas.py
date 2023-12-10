from pydantic import BaseModel


class NoteCreate(BaseModel):
    tg_id: int
    username: str


class NoteFull(BaseModel):
    tg_id: int
    username: str

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str


class TagFull(BaseModel):
    name: str

    class Config:
        from_attributes = True
