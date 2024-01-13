import disnake
from config import settings


class EchoClient(disnake.Client):
    async def on_message(self, message: disnake.Message):
        if message.author == client.user:
            return
        await message.reply(message.content)


client = EchoClient()
client.run(settings.DISCORD_TOKEN)
