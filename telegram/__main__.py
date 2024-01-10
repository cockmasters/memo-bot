import asyncio

from bot.bot import bot_setup, bot
from bot.dispatcher import registration_dispatcher, dp
from bot.log import start_logging


async def main():
    await bot_setup(bot)
    start_logging()
    registration_dispatcher(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
