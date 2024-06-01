from aiogram import types
from aiogram.filters import Command

from filters import IsGroup
from loader import dp, is_admin_filter


@dp.message(Command(commands=["chat_id"]), IsGroup(), is_admin_filter)
async def get_chat_id(message: types.Message):
    await message.delete()
    await message.answer(str(message.chat.id))


@dp.message(Command(commands=["sticker_id", "id"]), IsGroup())
async def get_sticker_id(message: types.Message):
    await message.delete()
