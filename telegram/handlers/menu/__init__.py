from aiogram import Router

from telegram.handlers.menu import add, all_notes


def router() -> Router:
    rout = Router()
    rout.include_routers(add.router, all_notes.router)
    return rout
