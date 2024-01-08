from typing import Optional

from pydantic import BaseModel, model_validator


class UserSocials(BaseModel):
    tg_id: Optional[int] = None
    vk_id: Optional[int] = None
    ds_id: Optional[int] = None

    @model_validator(mode="after")
    def check_for_none(self):
        if not (self.tg_id or self.vk_id or self.ds_id):
            raise ValueError("at least one id must be present")
        return self


class UserFull(BaseModel):
    id: int
    tg_id: Optional[int]
    vk_id: Optional[int]
    ds_id: Optional[int]

    class Config:
        from_attributes = True
