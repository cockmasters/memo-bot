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
    await state_dispenser.set(message.peer_id, AddNoteStates.BODY, body=message.text)


@labeler.message(state=AddNoteStates.BODY)
async def add_note_tags(message: Message):
    await state_dispenser.set(message.peer_id, AddNoteStates.TAGS, tags=message.text)
    await state_dispenser.delete(message.peer_id)
    await message.answer("Записка добавлена")


@labeler.message(text=["/get_all"])
async def get_all_notes(message: Message):
    await message.answer(format_notes([]))


@labeler.message(text=["/filter_title <title>"])
async def filter_by_title(message: Message, title: str):
    await message.answer(format_notes([]))


@labeler.message(text=["/filter_tags <tags>"])
async def filter_by_tags(message: Message, tags: str):
    tags: list[str] = format_tags(tags)
    await message.answer(format_notes([]))
