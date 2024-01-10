from bot.bot import bot
from config import bot_settings
from middlewares.bot_info.BotInfo import BotInfo

bot_info: BotInfo = BotInfo(
    bot_info_token=bot_settings.TG_TOKEN_BOT_LOG,
    admin=bot_settings.TG_ADMIN_BOT_LOG
)
bot_info.set_bot_title(bot)
