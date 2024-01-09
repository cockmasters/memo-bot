from backend_request.schemas import AuthKey
from vk import api
from vk.core.exception_handlers import handle_api_exception
from vk.core.middlewares import user_id
from vkbottle.bot import BotLabeler, Message

labeler = BotLabeler()


@labeler.message(text=["/link <code>"])
@handle_api_exception
async def link_by_code(message: Message, code: str):
    request_data = AuthKey(code=code)
    await api.link_account(user_id=user_id.get(), data=request_data)
    await message.answer("Аккаунт привязан")


@labeler.message(text=["/link"])
@handle_api_exception
async def get_link_code(message: Message):
    data = await api.get_auth_key(user_id=user_id.get())
    await message.answer(f"Код для привязки: {data.code}. Никому его не сообщайте.")
