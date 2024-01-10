from contextvars import ContextVar
from typing import Optional, Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from backend_request.api import BackendApi
from backend_request.schemas import CreateUserRequest
from telegram import api
from telegram.bot.bot import bot
from telegram.middlewares.update_to_tg_id import update_to_tg_id


class BackendApiExcMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: Dict[str, Any]
    ) -> Any:
        tg_id = update_to_tg_id(update)
        try:
            return await handler(update, data)
        except BackendApi.Error as exc:
            if not exc.message:
                await bot.send_message(chat_id=tg_id, text="Во время обработки запроса произошла ошибка")
            await bot.send_message(chat_id=tg_id, text=exc.message)

