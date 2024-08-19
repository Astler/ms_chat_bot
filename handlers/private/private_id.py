from aiogram import types, Router
from aiogram.filters import Command

from filters import IsPrivate
from utils.misc import rate_limit

id_router = Router()


@rate_limit()
@id_router.message(Command("id"), IsPrivate())
async def bot_help(message: types.Message):
    await message.answer(str(message.from_user.id))
