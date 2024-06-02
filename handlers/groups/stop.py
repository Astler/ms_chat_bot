from aiogram import types, Router
from aiogram.filters import Command

from filters import IsGroup

from utils.data.bot_data import save_bot_data, get_bot_data

stop_router = Router()


@stop_router.message(IsGroup(), Command("stop"))
async def start_bot(message: types.Message):
    chat_id = message.chat.id
    bot_data = get_bot_data()

    if bot_data.chats_to_notify.__contains__(chat_id):
        bot_data.chats_to_notify.remove(chat_id)
        await message.reply("Removed chat from automatic operations!")
        save_bot_data(bot_data)
        return

    await message.reply("Chat is not in auto commands list!")
