from aiogram import types, Router
from aiogram.filters import CommandObject, Command

from filters import IsGroup
from loader import is_admin_filter
from utils.data.bot_data import BotData
from utils.data.group_data import GroupInfo

lines_router = Router()


@lines_router.message(IsGroup(), is_admin_filter, Command(commands=["lines"]))
async def lines_command(message: types.Message, command: CommandObject):
    chat_id = message.chat.id
    bot_data = BotData.load()
    group_data = GroupInfo.load(chat_id)

    if command.args:
        action = command.args.lower()

        is_lines_exists = bot_data.lines_keys.__contains__(action) or action == "default"

        if is_lines_exists:
            group_data.lines_key = action
            group_data.save()
            await message.reply(f"Lines group changed to {action}.")
        else:
            await message.reply(f"Lines group {action} not found.")
    else:
        await message.reply("Add lines keys to select them!")

