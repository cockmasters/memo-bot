from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GetUserProfileResponse:
    id: int
    vk_id: Optional[str] = None
    tg_id: Optional[str] = None
    ds_id: Optional[str] = None


@dataclass
class CreateUserRequest:
    vk_id: Optional[str] = None
    tg_id: Optional[str] = None
    ds_id: Optional[str] = None


@dataclass
class CreateUserResponse:
    id: int
    vk_id: Optional[str] = None
    tg_id: Optional[str] = None
    ds_id: Optional[str] = None


@dataclass
class NoteCreateRequest:
    title: str
    body: str
    tags: list[str]


@dataclass
class Note:
    id: int
    user_id: int
    title: str
    body: str
    tags: list[str]
    created: datetime


@dataclass
class NoteCreateResponse(Note):
    pass


@dataclass
class FilterNotes:
    title: Optional[str] = None
    tags: Optional[list[str]] = None


@dataclass
class AuthKey:
    code: str
