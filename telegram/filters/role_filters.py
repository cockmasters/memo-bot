from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from config import bot_settings


class AdminFilter(BaseFilter):
    def __init__(self):
        super().__init__()

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        return update.from_user.id == bot_settings.TG_ADMIN
