from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GetUserProfileResponse:
    id: int
    username: str
    tg_id: Optional[int] = None


@dataclass
class CreateUserRequest:
    username: str
    tg_id: Optional[int] = None


@dataclass
class CreateUserResponse:
    id: int
    username: str
    tg_id: Optional[int] = None


@dataclass
class NoteCreateRequest:
    title: str
    body: str


@dataclass
class Note:
    title: str
    body: str
    created: datetime


@dataclass
class NoteCreateResponse(Note):
    pass
