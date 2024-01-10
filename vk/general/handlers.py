from vk.core.exception_handlers import handle_api_exception
from vkbottle.bot import BotLabeler, Message

labeler = BotLabeler()

welcome_message = """
Привет, я бот для записок.
Чтобы узнать о моих возможностях напишите - /help.
"""
help_message = """
Здесь вы можете оставлять свои записки.

Общие комманды:
/start - Показывает приветственное сообщение
/help - Показывает данное сообщение

Команды взаимодействия с записками:
/add - Добавление записки
/get_all - Показывает созданные записки
/filter_title <название> - Фильтрует записки по названию
/filter_tags <тег_1, тег_2, ...> - Фильтрует записки по множеству тегов

Команды для привязки аккаунта:
/link - Запрос авторизационного кода
/link <код> - Связывает аккаунт по авторизационному коду с текущим аккаунтом (объединяя записки обоих аккаунтов)
"""
unknown_message = """
Неизвестная комманда.
Чтобы узнать о моих возможностях напишите - /help.
"""


@labeler.message(text=["/start"])
@handle_api_exception
async def greetings(message: Message):
    await message.answer(welcome_message)


@labeler.message(text=["/help"])
@handle_api_exception
async def help(message: Message):
    await message.answer(help_message)


@labeler.message()
@handle_api_exception
async def unknown_command(message: Message):
    await message.answer(unknown_message)
