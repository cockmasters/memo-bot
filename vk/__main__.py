from backend_request.api import BackendApi
from vk.config import settings
from vk.core.middlewares import UserMiddleware
from vk.note.handlers import labeler as note_labeler
from vk.note.states import state_dispenser
from vk.user.handlers import labeler as user_labeler
from vkbottle.bot import Bot

bot = Bot(settings.VK_GROUP_TOKEN, state_dispenser=state_dispenser)


@bot.error_handler.register_error_handler(BackendApi.Error)
async def forward_error_from_api(e: BackendApi.Error):
    pass


for labeler in [user_labeler, note_labeler]:
    bot.labeler.load(labeler)
bot.labeler.message_view.register_middleware(UserMiddleware)
bot.run_forever()
