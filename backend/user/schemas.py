from pydantic import BaseModel


class UserCreate(BaseModel):
    tg_id: int
    username: str


class UserFull(BaseModel):
    tg_id: int
    username: str

    class Config:
        from_attributes = True
