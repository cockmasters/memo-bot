from config import settings
from vkbottle.bot import Bot, Message

bot = Bot(settings.VK_GROUP_TOKEN)


@bot.on.message()
async def handler(message: Message) -> str:
    await message.answer(message.text)


bot.run_forever()
