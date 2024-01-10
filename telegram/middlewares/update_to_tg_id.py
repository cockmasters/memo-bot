from aiogram.types import Update


def update_to_tg_id(update: Update) -> int:
    tg_id = None
    if update.message is not None:
        tg_id = update.message.from_user.id
    elif update.callback_query is not None:
        tg_id = update.callback_query.from_user.id
    else:
        tg_id = update.inline_query.from_user.id
    return tg_id
