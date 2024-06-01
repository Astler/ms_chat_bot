from aiogram import types
from aiogram.filters import Command

from filters import IsPrivate
from loader import dp
from utils.misc import rate_limit


@rate_limit()
@dp.message(IsPrivate(), Command("id"))
async def get_my_id(message: types.Message):
    await message.answer(f'Ваш id: {message.from_user.id}')

