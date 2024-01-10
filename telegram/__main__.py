import asyncio

from telegram.bot.bot import bot_setup, bot
from telegram.bot.dispatcher import registration_dispatcher, dp
from telegram.bot.log import start_logging


async def main():
    await bot_setup(bot)
    start_logging()
    registration_dispatcher(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
