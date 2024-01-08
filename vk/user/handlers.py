from vkbottle.bot import BotLabeler, Message

labeler = BotLabeler()


@labeler.message(text=["/link <code>"])
async def link_by_code(message: Message, code: int):
    await message.answer("Аккаунт привязан")


@labeler.message(text=["/link"])
async def get_link_code(message: Message):
    code = 123
    await message.answer(f"Код для привязки: {code}. Никому его не сообщайте.")
