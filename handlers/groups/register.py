from aiogram import types, Router, Bot
from aiogram.filters import CommandObject, Command
from pyrogram.errors import ChannelInvalid

from data.to_export import my_id
from filters import IsGroup
from filters.is_specific_user import IsSpecificUser
from utils.data.group_data import GroupInfo
from utils.misc.common import create_user_mention

register_router = Router()


@register_router.message(IsGroup(), Command(commands=["join"]))
async def join_command(message: types.Message, command: CommandObject):
    chat_id = message.chat.id
    group_data = GroupInfo.load(chat_id)
    user_id = message.from_user.id

    if user_id in group_data.registered_users:
        await message.reply("Already in!")
    else:
        group_data.registered_users.append(user_id)
        group_data.save()
        await message.reply("Added to registered users list!")


@register_router.message(IsGroup(), Command(commands=["joined"]))
async def join_command(message: types.Message, bot: Bot):
    all_in_chat = []
    chat_id = message.chat.id
    group_data = GroupInfo.load(chat_id)

    try:
        for member in await group_data.get_available_non_bot_chat_members():
            all_in_chat.append(create_user_mention(member))
        await bot.send_message(message.chat.id, "\n".join(all_in_chat), parse_mode="Markdown")
    except ChannelInvalid as e:
        await message.reply(f"I cannot access the members of this group or channel. Exception details: {e}")
    except Exception as e:
        await message.reply(f"An error occurred while retrieving chat members: {e}")


@register_router.message(IsGroup(), Command(commands=["leave"]))
async def leave_command(message: types.Message, command: CommandObject):
    chat_id = message.chat.id
    group_data = GroupInfo.load(chat_id)
    user_id = message.from_user.id

    if user_id in group_data.registered_users:
        group_data.registered_users.remove(user_id)
        group_data.save()
        await message.reply("Removed from registered users list!")
    else:
        await message.reply("You are not in registered users list!")
