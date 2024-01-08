from vk.config import settings
from vk.core.middlewares import UserMiddleware
from vk.note.handlers import labeler as note_labeler
from vk.note.states import state_dispenser
from vk.user.handlers import labeler as user_labeler
from vkbottle.bot import Bot

bot = Bot(settings.VK_GROUP_TOKEN, state_dispenser=state_dispenser)


for labeler in [user_labeler, note_labeler]:
    bot.labeler.load(labeler)
bot.labeler.message_view.register_middleware(UserMiddleware)
bot.run_forever()
