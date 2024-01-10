from typing import Optional

from pydantic import BaseModel, model_validator
from user.exceptions import EmptyUserSocials


class UserSocials(BaseModel):
    tg_id: Optional[str] = None
    vk_id: Optional[str] = None
    ds_id: Optional[str] = None

    @model_validator(mode="after")
    def check_for_none(self):
        if not (self.tg_id or self.vk_id or self.ds_id):
            raise EmptyUserSocials
        return self


class UserFull(BaseModel):
    id: int
    tg_id: Optional[str]
    vk_id: Optional[str]
    ds_id: Optional[str]

    class Config:
        from_attributes = True


class UserCode(BaseModel):
    code: str
