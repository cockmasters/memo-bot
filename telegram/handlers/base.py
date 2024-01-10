from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()


@router.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = [[
        InlineKeyboardButton(
            text="Открыть инлайн режим бота",
            switch_inline_query_current_chat=""
        )
    ]]
    await message.answer(text=f'Привет, я бот для погоды\n\n'
                              f'Вы можете воспользоваться мной в любом чате. '
                              f'Введите @inline_weather_bot и потом начните писать свой город'
                              f' или нажмите кнопку под этим сообщением.\n\n'
                              f'Приятного использования!',
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
                         )


@router.message(Command("help"))
async def help_cmd(message: types.Message):
    kb = [[
        InlineKeyboardButton(
            text="Открыть инлайн режим бота",
            switch_inline_query_current_chat=""
        )
    ]]
    await message.answer(text=f'Я бот для погоды\n\n'
                              f'Вы можете воспользоваться мной в любом чате. '
                              f'Введите @inline_weather_bot и потом начните писать свой город'
                              f' или нажмите кнопку под этим сообщением.\n\n'
                              f'Бот позволяет узнать погоду:\n'
                              f'1) Погоду в данный момент\n'
                              f'2) Погоду на будущее с шагом в 3 часа\n'
                              f'3) Погоду на будущие дни\n'
                              f'(в 12 часов дня)\n'
                              f'\nЕсли вашего города нет в списке, напишите об этом боту и возможно город добавят.\n\n'
                              f'Приятного использования!',

                         reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
                         )
