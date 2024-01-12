from aiogram import Router, types, F

from telegram import api
from telegram.bot.bot import bot
from telegram.keyboards.inline import NoteCallbackFactory
from telegram.middlewares.UserMiddleware import user_id

router = Router()


@router.callback_query(NoteCallbackFactory.filter(F.action == "delete"))
async def add_note_cb(
    callback: types.CallbackQuery,
    callback_data: NoteCallbackFactory,
):
    await api.delete_note(user_id=user_id.get(), note_id=callback_data.note_id)
    await bot.edit_message_text(
        inline_message_id=callback.inline_message_id,
        text='Записка удалена!!',
    )
