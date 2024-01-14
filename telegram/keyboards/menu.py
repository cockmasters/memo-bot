from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallbackFactory(CallbackData, prefix="fab_menu"):
    action: str


def menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добавить записку",
        callback_data=MenuCallbackFactory(action="add_note")
    )
    builder.add(InlineKeyboardButton(
            text="Показать все записки",
            switch_inline_query_current_chat="title "
        ))
    builder.add(InlineKeyboardButton(
            text="Найти записку по тегам",
            switch_inline_query_current_chat="tags "
    ))
    builder.add(InlineKeyboardButton(
        text="Найти записку по названию с сортировкой по дате",
        switch_inline_query_current_chat="date "
    ))
    builder.adjust(1)
    return builder.as_markup()
