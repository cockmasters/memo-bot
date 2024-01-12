from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class NoteCallbackFactory(CallbackData, prefix="fab_note"):
    action: str
    note_id: int


def note_keyboard(note_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Изменить",
        callback_data=NoteCallbackFactory(action="edit", note_id=note_id)
    )
    builder.button(
        text="Удалить",
        callback_data=NoteCallbackFactory(action="delete", note_id=note_id)
    )
    builder.adjust(1)
    return builder.as_markup()


def not_notes_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Показать все записки",
        switch_inline_query_current_chat="title "
    ))
    builder.add(InlineKeyboardButton(
        text="Найти записку по тегам",
        switch_inline_query_current_chat="tags "
    ))
    builder.adjust(1)
    return builder.as_markup()
