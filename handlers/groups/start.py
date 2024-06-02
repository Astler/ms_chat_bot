from aiogram import types, Router
from aiogram.filters import CommandStart

from filters import IsGroup

from utils.data.bot_data import get_bot_data, save_bot_data

start_router = Router()


@start_router.message(IsGroup(), CommandStart())
async def start_bot(message: types.Message):
    chat_id = message.chat.id
    bot_data = get_bot_data()

    if bot_data.chats_to_notify.__contains__(chat_id):
        await message.reply("Already in!")
        return

    bot_data.chats_to_notify.append(chat_id)

    save_bot_data(bot_data)

    await message.reply("Added to automatic commands list!")
