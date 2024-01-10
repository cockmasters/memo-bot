from aiogram import Bot
from aiogram.types import BotCommand

from telegram.config import bot_settings

bot = Bot(token=bot_settings.TG_TOKEN)

bot_title = None


async def bot_setup(aiogram_bot: Bot) -> None:
    await aiogram_bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Запуск бота"),
            BotCommand(command="link", description="Привязка аккаунтов"),
            BotCommand(command="help", description="Полезная информация о боте")
        ]
    )


async def stop_bot(aiogram_bot: Bot):
    await aiogram_bot.close()
