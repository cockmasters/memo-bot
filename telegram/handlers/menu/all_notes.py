from typing import List

from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from backend_request.schemas import Note
from telegram import api
from telegram.middlewares.UserMiddleware import user_id

router = Router()


class DefaultResults:
    not_found = [InlineQueryResultArticle(
        id="1",
        title="Не могу найти записки!!",
        description="Вероятно вы не писали записок с такими параметрами((",
        input_message_content=InputTextMessageContent(
            message_text=f'Записки не найдены!!\n\n'
        )
    )]


@router.inline_query()
async def show_all_notes(inline_query: InlineQuery):
    notes: List[Note] = await api.get_notes_all(user_id=user_id.get())
    results = []
    for note in notes:
        results.append(
            InlineQueryResultArticle(
                id=str(note.id),
                title=note.title,
                description="Показать записку!",
                input_message_content=InputTextMessageContent(
                    message_text=f'{note.body}',
                ),
            )
        )
    if not results:
        results = DefaultResults.not_found
    await inline_query.answer(results, is_personal=True, cache_time=0)
