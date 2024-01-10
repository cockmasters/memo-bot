from aiogram import Dispatcher

from telegram.bot.bot_info import bot_info
from telegram.handlers import base, user, menu
from telegram.middlewares.BackendApiExcMiddleware import BackendApiExcMiddleware
from telegram.middlewares.bot_info.LogMiddleware import LogMiddleware
from telegram.middlewares.bot_info.NewUserMiddleware import NewUserMiddleware
from telegram.middlewares.UserMiddleware import UserMiddleware
from telegram.utils.root_dir import root_path

dp = Dispatcher()


def registration_dispatcher(dispatcher: Dispatcher) -> None:
    dispatcher.update.outer_middleware(BackendApiExcMiddleware())
    dispatcher.update.outer_middleware(LogMiddleware(
        bot_info=bot_info,
        path_log_file=root_path() / "log.log",
        clean_log=True,
        limit_counter=30
    ))
    dispatcher.update.outer_middleware(NewUserMiddleware(bot_info=bot_info))
    dispatcher.update.outer_middleware(UserMiddleware())
    dispatcher.include_routers(base.router, user.router, menu.router())
