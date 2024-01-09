# TODO: обернуть в транзакцию
from sqlalchemy.ext.asyncio import AsyncSession
from user.models import User
from user.note.models import Note


async def merge_accounts(user_id_1: int, user_id_2: int, session: AsyncSession):
    user_1: User = await User.get_by_id(user_id_1, session)
    user_2: User = await User.get_by_id(user_id_2, session)
    new_user: User = await User.create(session=session)

    # прикрепляет записки старых юзеров к новому
    await Note.replace_author(user_1.id, new_user.id, session)
    await Note.replace_author(user_2.id, new_user.id, session)

    # удаление старых юзеров
    await User.delete(user_1.id, session)
    await User.delete(user_2.id, session)

    await session.flush()

    # сливает данные старых юзеров в нового
    new_user.tg_id = user_1.tg_id or user_2.tg_id
    new_user.vk_id = user_1.vk_id or user_2.vk_id
    new_user.ds_id = user_1.ds_id or user_2.ds_id

    await session.commit()
