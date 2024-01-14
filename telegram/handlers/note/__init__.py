from aiogram import Router

from telegram.handlers.note import delete, edit


def router() -> Router:
    rout = Router()
    rout.include_routers(delete.router, edit.router)
    return rout
