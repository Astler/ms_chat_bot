from aiogram import types, Router, Bot
from aiogram.filters import Command
from pyrogram.errors import ChannelInvalid

from utils.misc.common import create_user_mention

all_router = Router()


@all_router.message(Command(commands=["members", "abroad"]))
async def users_in_this_chat(message: types.Message, bot: Bot):
    all_in_chat = []

    try:
        chat_type = message.chat.type
        print(message.chat.id)
        if chat_type in ["group", "supergroup"]:
            from loader import pyro_client
            async for member in pyro_client.get_chat_members(message.chat.id):
                all_in_chat.append(create_user_mention(member))
        else:
            raise ChannelInvalid("This command is only supported in groups and supergroups.")

        await bot.send_message(message.chat.id, "\n".join(all_in_chat), parse_mode="Markdown")
    except ChannelInvalid as e:
        await message.reply(f"I cannot access the members of this group or channel. Exception details: {e}")
    except Exception as e:
        await message.reply(f"An error occurred while retrieving chat members: {e}")
