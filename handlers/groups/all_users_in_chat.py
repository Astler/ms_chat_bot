from aiogram import types
from pyrogram.errors import ChannelInvalid

from loader import dp, bot, app
from utils.misc.common import create_user_mention


@dp.message_handler(commands=["members", "abroad"])
async def users_in_this_chat(message: types.Message):
    all_in_chat = []

    try:
        chat_type = message.chat.type
        print(message.chat.id)
        if chat_type in ["group", "supergroup"]:
            async for member in app.get_chat_members(message.chat.id):
                all_in_chat.append(create_user_mention(member))
        else:
            raise ChannelInvalid("This command is only supported in groups and supergroups.")

        await bot.send_message(message.chat.id, "\n".join(all_in_chat), parse_mode="Markdown")
    except ChannelInvalid as e:
        await bot.send_message(message.chat.id,
                               f"I cannot access the members of this group or channel. Exception details: {e}")
    except Exception as e:
        await bot.send_message(message.chat.id, f"An error occurred while retrieving chat members: {e}")
