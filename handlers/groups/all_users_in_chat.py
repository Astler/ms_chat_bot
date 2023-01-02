from aiogram import types

from loader import dp, bot, app
from utils.misc.common import create_user_mention


@dp.message_handler(commands=["members", "abroad"])
async def users_in_this_chat(message: types.Message):
    all_in_chat = []

    async for member in app.get_chat_members(message.chat.id):
        all_in_chat.append(create_user_mention(member))

    await bot.send_message(message.chat.id, "\n".join(all_in_chat), parse_mode="Markdown")
