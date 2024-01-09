from functools import wraps

from backend_request.api import BackendApi
from vkbottle.bot import Message


def handle_api_exception(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)
        except BackendApi.Error as exc:
            if not exc.message:
                await message.answer("Во время обработки запроса произошла ошибка")
            await message.answer(exc.message)

    return wrapper
