from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from backend_request.schemas import NoteCreateRequest
from telegram import api
from telegram.bot.bot import bot
from telegram.handlers.menu.all_notes import format_note
from telegram.keyboards.inline import NoteCallbackFactory
from telegram.middlewares.UserMiddleware import user_id

router = Router()


class EditNoteState(StatesGroup):
    add_title = State()
    add_body = State()
    add_tags = State()


@router.callback_query(NoteCallbackFactory.filter(F.action == "edit"))
async def add_note_cb(
    callback: types.CallbackQuery,
    callback_data: NoteCallbackFactory,
    state: FSMContext
):
    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Введите заголовок записки!!"
    )
    await callback.answer()
    await state.set_state(EditNoteState.add_title)
    await state.set_data(data={'note_id': callback_data.note_id})


@router.message(EditNoteState.add_title)
async def add_note_title(
    message: types.Message,
    state: FSMContext
):
    if message.text is None:
        await message.answer(text="Попробуйте ввести текст ещё раз!!")
        await state.set_state(EditNoteState.add_title)
        return
    note = NoteCreateRequest(
        title=message.text,
        body="",
        tags=[]
    )
    await message.answer(text="Хорошо, теперь введите текст записки!!")
    await state.set_state(EditNoteState.add_body)
    await state.set_data(
        data={'note': note,
              'note_id': (await state.get_data())['note_id']}
    )


@router.message(EditNoteState.add_body)
async def add_episode_data(
    message: types.Message,
    state: FSMContext
):
    if message.text is None:
        await message.answer(text="Попробуйте ввести текст ещё раз!!")
        await state.set_state(EditNoteState.add_body)
        return
    note: NoteCreateRequest = (await state.get_data())['note']
    note.body = message.text
    await message.answer(text="Хорошо, теперь введите теги через запятую, заменяя пробелы на _ !!")
    await state.set_state(EditNoteState.add_tags)
    await state.set_data(
        data={'note': note,
              'note_id': (await state.get_data())['note_id']}
    )


@router.message(EditNoteState.add_tags)
async def add_episode_data(
    message: types.Message,
    state: FSMContext
):
    if message.text is None:
        await message.answer(text="Попробуйте ввести текст ещё раз!!")
        await state.set_state(EditNoteState.add_body)
        return
    note: NoteCreateRequest = (await state.get_data())['note']
    note.tags = [i.replace(" ", "") for i in message.text.split(",")]
    note_id = (await state.get_data())['note_id']

    note_edit = await api.edit_note(data=note, note_id=note_id)
    await message.answer(text="Записка изменена!!")
    await message.answer(text=format_note(note_edit))
    await state.clear()
