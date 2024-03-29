from aiogram import Router, types
from aiogram.filters import Command

from telegram.keyboards.menu import menu_keyboard

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(text=f'Привет, я бот для записок!!\n\n',
                         reply_markup=menu_keyboard())


@router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(text=f'Здесь вы можете написать свои записки!!\n\n'
                              f'Вам доступны следующие команды:\n'
                              f'/start - открывает меню\n'
                              f'/link - без параметров выдаёт код для связывания аккаунтов, '
                              f'с параметрами принимает код для связывания этого аккаунта с другими соцсетями\n'
                              f'/help - помощь по боту\n'
                              f'В меню вы можете добавить записку или найти записку по тегам или названию\n'
                              f'Записку можно удалить или изменить!!')




