from typing import List

from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from backend_request.schemas import Note, FilterNotes
from telegram import api
from telegram.keyboards.inline import note_keyboard, not_notes_keyboard
from telegram.middlewares.UserMiddleware import user_id

router = Router()


class DefaultResults:
    not_found = [InlineQueryResultArticle(
        id="1",
        title="Не могу найти записки!!",
        description="Вероятно вы не писали записок с такими параметрами((",
        input_message_content=InputTextMessageContent(
            message_text=f'Записки не найдены!!\n\n'
        ),
        reply_markup=not_notes_keyboard()
    )]
    tag_default = [InlineQueryResultArticle(
        id="1",
        title="Введите тег полностью",
        description="На данный момент не могу найти такого тега",
        input_message_content=InputTextMessageContent(
            message_text=f'Записки не найдены!!\n\n'
        ),
        reply_markup = not_notes_keyboard()
    )]


def format_note(note: Note):
    text = (f'{note.title}\n\n'
            f'{note.body}\n\n'
            f'Теги: ')
    for tag in note.tags:
        text += (tag + ",")

    return text[:len(text) - 1]


def inline_results(notes: List[Note], flag_chat_with_bot: bool) -> List[InlineQueryResultArticle]:
    results = []
    for note in notes:
        if flag_chat_with_bot:
            results.append(
                InlineQueryResultArticle(
                    id=str(note.id),
                    title=note.title,
                    description="Показать записку!",
                    input_message_content=InputTextMessageContent(
                        message_text=f'{format_note(note)}',
                    ),
                    reply_markup=note_keyboard(note.id)
                )
            )
        else:
            results.append(
                InlineQueryResultArticle(
                    id=str(note.id),
                    title=note.title,
                    description="Показать записку!",
                    input_message_content=InputTextMessageContent(
                        message_text=f'{format_note(note)}',
                    ),
                )
            )

    return results


@router.inline_query(F.query.startswith("tags"))
async def show_all_tags(inline_query: InlineQuery):
    query: str = inline_query.query.replace("tags", "")
    query = query.strip()
    tags: list[str] = query.replace(" ", "").split(",")
    filter_args = FilterNotes(tags=tags)
    notes = await api.filter_notes(data=filter_args, user_id=user_id.get())

    flag_chat_with_bot = False
    if inline_query.chat_type is not None and inline_query.chat_type == "sender":
        flag_chat_with_bot = True

    results = inline_results(notes, flag_chat_with_bot)

    if not results:
        results = DefaultResults.not_found
    await inline_query.answer(results, is_personal=True, cache_time=0)


@router.inline_query(F.query.startswith("title"))
async def show_all_notes(inline_query: InlineQuery):
    notes: List[Note] = await api.get_notes_all(user_id=user_id.get())
    query = inline_query.query.replace("title", "")
    query = query.strip()
    if query is not None and query != "":
        filter_notes = []
        for note in notes:
            if query in note.title:
                filter_notes.append(note)
        filter_notes.sort(key=lambda x: x.title.startswith(query), reverse=True)
        notes = filter_notes

    flag_chat_with_bot = False
    if inline_query.chat_type is not None and inline_query.chat_type == "sender":
        flag_chat_with_bot = True

    results = inline_results(notes, flag_chat_with_bot)

    if not results:
        results = DefaultResults.not_found
    await inline_query.answer(results, is_personal=True, cache_time=0)
