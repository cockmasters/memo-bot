from backend_request.schemas import FilterNotes, NoteCreateRequest
from vk import api
from vk.core.middlewares import user_id
from vk.note.formatter import format_notes, format_tags
from vk.note.states import AddNoteStates, state_dispenser
from vkbottle.bot import BotLabeler, Message

labeler = BotLabeler()


@labeler.message(text=["/add"])
async def add_note(message: Message):
    await message.answer("Введите название новой записки.")
    await state_dispenser.set(message.peer_id, AddNoteStates.STARTED)


@labeler.message(state=AddNoteStates.STARTED)
async def add_note_title(message: Message):
    await message.answer("Введите текст новой записки.")
    await state_dispenser.set(message.peer_id, AddNoteStates.TITLE, title=message.text)


@labeler.message(state=AddNoteStates.TITLE)
async def add_note_body(message: Message):
    await message.answer("Введите список тегов для новой записки. В следующем формате: тег_1, тег_2")
    state = await state_dispenser.get(message.peer_id)
    await state_dispenser.set(message.peer_id, AddNoteStates.BODY, body=message.text, **state.payload)


@labeler.message(state=AddNoteStates.BODY)
async def add_note_tags(message: Message):
    tags = format_tags(message.text)
    state = await state_dispenser.get(message.peer_id)
    await state_dispenser.set(message.peer_id, AddNoteStates.TAGS, tags=tags, **state.payload)

    state = await state_dispenser.get(message.peer_id)
    note = NoteCreateRequest(**state.payload)
    await api.create_note(data=note, user_id=user_id.get())

    await state_dispenser.delete(message.peer_id)
    await message.answer("Записка добавлена")


@labeler.message(text=["/get_all"])
async def get_all_notes(message: Message):
    notes = await api.get_notes_all(user_id=user_id.get())
    await message.answer(format_notes(notes))


@labeler.message(text=["/filter_title <title>"])
async def filter_by_title(message: Message, title: str):
    filter_args = FilterNotes(title=title)
    notes = await api.filter_notes(data=filter_args, user_id=user_id.get())
    await message.answer(format_notes(notes))


@labeler.message(text=["/filter_tags <tags>"])
async def filter_by_tags(message: Message, tags: str):
    tags: list[str] = format_tags(tags)
    filter_args = FilterNotes(tags=tags)
    notes = await api.filter_notes(data=filter_args, user_id=user_id.get())
    await message.answer(format_notes(notes))
