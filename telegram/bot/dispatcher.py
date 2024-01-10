from aiogram import Dispatcher

from bot.bot_info import bot_info
from handlers import base
from middlewares.bot_info.LogMiddleware import LogMiddleware
from middlewares.bot_info.NewUserMiddleware import NewUserMiddleware
from utils.root_dir import root_path

dp = Dispatcher()


def registration_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.update.outer_middleware(LogMiddleware(
        bot_info=bot_info,
        path_log_file=root_path() / "log.log",
        clean_log=True,
        limit_counter=30
    ))
    dispatcher.update.outer_middleware(NewUserMiddleware(bot_info=bot_info))
    dispatcher.include_routers(base.router)
