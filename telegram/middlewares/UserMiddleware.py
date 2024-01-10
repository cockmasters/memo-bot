from contextvars import ContextVar
from typing import Optional, Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from backend_request.api import BackendApi
from backend_request.schemas import CreateUserRequest
from telegram import api
from telegram.bot.bot import bot

user_id: ContextVar[Optional[int]] = ContextVar("user_id", default=None)


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: Dict[str, Any]
    ) -> Any:
        tg_id = None
        if update.message is not None:
            tg_id = update.message.from_user.id
        elif update.callback_query is not None:
            tg_id = update.callback_query.from_user.id
        else:
            tg_id = update.inline_query.from_user.id

        try:
            profile = await api.get_by_socials_tg(tg_id=tg_id)
        except BackendApi.Error:
            user = CreateUserRequest(tg_id=tg_id)
            profile = await api.create_user(data=user)
            await bot.send_message(chat_id=tg_id, text="Аккаунт создан!")

        user_id.set(profile.id)

        return await handler(update, data)
