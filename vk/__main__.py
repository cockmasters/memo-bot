from vk.config import settings
from vk.core.middlewares import UserMiddleware
from vk.general.handlers import labeler as general_labeler
from vk.note.handlers import labeler as note_labeler
from vk.note.states import state_dispenser
from vk.user.handlers import labeler as user_labeler
from vkbottle.bot import Bot

bot = Bot(settings.VK_GROUP_TOKEN, state_dispenser=state_dispenser)


for labeler in [user_labeler, note_labeler, general_labeler]:
    bot.labeler.load(labeler)

for middleware in [UserMiddleware]:
    bot.labeler.message_view.register_middleware(middleware)

bot.run_forever()
