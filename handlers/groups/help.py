from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Технические',
        '/id - бот вернет ваш id в TG (только в ЛС!)\n'
    ]

    formatted_text = '\n'.join(text)

    await message.answer(formatted_text)
