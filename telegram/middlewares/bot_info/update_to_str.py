from datetime import datetime, timedelta

from aiogram.types import Message, Update, CallbackQuery, InlineQuery


def general_to_str(obj: Message | CallbackQuery | InlineQuery):
    date = "Не задано"
    if hasattr(obj, 'date'):
        date = obj.date + timedelta(hours=3)
    return (f'Пользователь: {obj.from_user.full_name}\n'
            f'Chat_ID(ID): {obj.from_user.id}\n'
            f'Ссылка: {obj.from_user.username}\n'
            f'Время обработки: {datetime.utcnow() + timedelta(hours=3)}\n'
            f'Время в update: {date}\n'
            )


def message_to_str(message: Message) -> str:
    return general_to_str(message) + f'Написал: {message.text}\n'


def callback_to_str(callback: CallbackQuery) -> str:
    return general_to_str(callback) + f'Отправил callback: {callback.data}\n'


def inline_query_to_str(inline_query: InlineQuery) -> str:
    return general_to_str(inline_query) + (
        f'Отправил inline_query: {inline_query.query}\n'
        f'Chat_Type: {inline_query.chat_type}\n'
    )


def update_to_str(update: Update):
    log = f'\nUpdate: {update.update_id}\n'
    if update.message is not None:
        log += message_to_str(update.message)
    elif update.callback_query is not None:
        log += callback_to_str(update.callback_query)
    elif update.inline_query is not None:
        log += inline_query_to_str(update.inline_query)

    return log
