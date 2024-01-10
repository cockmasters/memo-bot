from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from backend_request.schemas import NoteCreateRequest
from telegram import api
from telegram.keyboards.menu import MenuCallbackFactory
from telegram.middlewares.UserMiddleware import user_id

router = Router()


class AddNoteState(StatesGroup):
    add_title = State()
    add_body = State()
    add_tags = State()


@router.callback_query(MenuCallbackFactory.filter(F.action == "add_note"))
async def add_note_cb(
    callback: types.CallbackQuery,
    callback_data: MenuCallbackFactory,
    state: FSMContext
):
    await callback.message.answer("Введите заголовок записки!!")
    await callback.answer()
    await state.set_state(AddNoteState.add_title)


@router.message(AddNoteState.add_title)
async def add_note_title(
    message: types.Message,
    state: FSMContext
):
    if message.text is None:
        await message.answer(text="Попробуйте ввести текст ещё раз!!")
        await state.set_state(AddNoteState.add_title)
        return
    note = NoteCreateRequest(
        title=message.text,
        body="",
        tags=[]
    )
    await message.answer(text="Хорошо, теперь введите текст записки!!")
    await state.set_state(AddNoteState.add_body)
    await state.set_data(data={'note': note})


@router.message(AddNoteState.add_body)
async def add_episode_data(
    message: types.Message,
    state: FSMContext
):
    if message.text is None:
        await message.answer(text="Попробуйте ввести текст ещё раз!!")
        await state.set_state(AddNoteState.add_body)
        return
    note: NoteCreateRequest = (await state.get_data())['note']
    note.body = message.text
    await message.answer(text="Хорошо, теперь введите теги через запятую, заменяя пробелы на _ !!")
    await state.set_state(AddNoteState.add_tags)
    await state.set_data(data={'note': note})


@router.message(AddNoteState.add_tags)
async def add_episode_data(
    message: types.Message,
    state: FSMContext
):
    if message.text is None:
        await message.answer(text="Попробуйте ввести текст ещё раз!!")
        await state.set_state(AddNoteState.add_body)
        return
    note: NoteCreateRequest = (await state.get_data())['note']
    note.tags = [i.replace(" ", "") for i in message.text.split(",")]

    await api.create_note(data=note, user_id=user_id.get())
    await message.answer(text="Записка добавлена!!")
    await state.clear()
