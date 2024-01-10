import asyncio

from aiogram import Bot


class NoBotTitleException(Exception):
    pass


class BotInfo:
    def __init__(self, bot_info_token: str, admin: int):
        self.bot = Bot(token=bot_info_token)
        self.admin = admin
        self.__bot_title: str

    @property
    def bot_title(self) -> str:
        if self.__bot_title is None:
            raise NoBotTitleException
        return self.__bot_title

    # __func не делать переменной с ключом иначе не работает
    async def send_partial(self, __func, **kwargs):
        await __func(chat_id=self.admin, **kwargs)

    def set_bot_title(self, bot: Bot):
        bot_user = asyncio.run(bot.me())
        asyncio.run(bot.session.close())
        self.__bot_title = (f'#{bot_user.username}\n'
                            f'Bot @{bot_user.username} id={bot.id} - {bot_user.full_name}')
