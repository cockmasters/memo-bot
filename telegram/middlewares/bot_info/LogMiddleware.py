import asyncio
import logging
from pathlib import PurePath, Path

from typing import Callable, Dict, Any, Awaitable, Optional
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, FSInputFile

from bot.bot import bot
from config import bot_settings
from middlewares.bot_info.BotInfo import BotInfo
from middlewares.bot_info.update_to_str import update_to_str


class LogMiddleware(BaseMiddleware):
    def __init__(
        self,
        bot_info: Optional[BotInfo] = None,
        path_log_file: Optional[PurePath] = None,
        clean_log: bool = False,
        limit_counter: int = 100
    ):
        self.bot_info = bot_info
        self.path_log_file = path_log_file
        self.clean_log = clean_log
        self.limit_counter = limit_counter
        self.is_init_bot_info = False

        if self.bot_info is not None and self.path_log_file is not None:
            self.is_init_bot_info = True
        self.counter: int = 0

    async def send_file_log(self):
        self.counter += 1
        if self.counter >= self.limit_counter:
            document = FSInputFile(filename="log.log", path=Path(self.path_log_file))
            await self.bot_info.send_partial(
                self.bot_info.bot.send_document,
                document=document,
                caption=self.bot_info.bot_title
            )
            if self.clean_log:
                open(file=self.path_log_file, mode='w').close()

            self.counter = 0

    def bot_log(self, update: Update):
        try:
            log = update_to_str(update)
            if log is not None:
                logging.info(log)
                if self.is_init_bot_info:
                    asyncio.create_task(self.send_file_log())
        except Exception as ex:
            text = (f'Ошибка при записи логов!!\n'
                    f'{ex}\n')
            logger = logging.getLogger(__name__)
            logger.error(text)
            asyncio.create_task(bot.send_message(chat_id=bot_settings.TG_ADMIN, text=text))

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: Dict[str, Any]
    ) -> Any:
        self.bot_log(update)

        return await handler(update, data)
