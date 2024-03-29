from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), AdminFilter(), commands=["chat_id"])
async def get_chat_id(message: types.Message):
    await message.delete()
    await message.answer(message.chat.id)


@dp.message_handler(IsGroup(), commands=["sticker_id", "id"])
async def get_chat_id(message: types.Message):
    await message.delete()
