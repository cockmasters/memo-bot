from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from backend_request.schemas import AuthKey
from telegram import api
from telegram.middlewares.UserMiddleware import user_id

router = Router()


@router.message(Command("link"))
async def link_by_code(message: Message, command: CommandObject):
    if command.args is None:
        data = await api.get_auth_key(user_id=user_id.get())
        await message.answer(f"Код для привязки: {data.code}. Никому его не сообщайте.")
        return

    request_data = AuthKey(code=command.args.replace(" ", ""))
    await api.link_account(user_id=user_id.get(), data=request_data)
    await message.answer("Аккаунт привязан")
