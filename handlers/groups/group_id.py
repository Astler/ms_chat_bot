from aiogram import types, Router
from aiogram.filters import Command

from filters import IsGroup
from loader import is_admin_filter

tech_router = Router()


@tech_router.message(Command(commands=["chat_id"]), IsGroup(), is_admin_filter)
async def get_chat_id(message: types.Message):
    await message.delete()
    await message.answer(str(message.chat.id))
