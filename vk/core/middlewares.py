from contextvars import ContextVar
from typing import Optional

from backend_request.api import BackendApi
from backend_request.schemas import CreateUserRequest
from vk import api
from vkbottle import BaseMiddleware
from vkbottle.bot import Message

user_id: ContextVar[Optional[int]] = ContextVar("user_id", default=None)


class UserMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        vk_user = await self.event.get_user()
        try:
            profile = await api.get_by_socials(vk_id=vk_user.id)
        except BackendApi.Error:
            user = CreateUserRequest(vk_id=vk_user.id)  # TODO: fixme
            profile = await api.create_user(data=user)
        user_id.set(profile.id)
