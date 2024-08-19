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


@lines_router.message(IsGroup(), is_admin_filter, Command(commands=["add_line"]))
async def add_line_command(message: types.Message, command: CommandObject):
    bot_data = BotData.load()

    if command.args:
        args = command.args.split(' ', 1)
        if len(args) == 2:
            key, value = args[0].lower(), args[1].strip()

            if key in bot_data.lines_keys:
                bot_data.lines_keys[key].append(value)
            else:
                bot_data.lines_keys[key] = [value]

            bot_data.save()
            await message.reply(f"Added line to {key}: {value}")
        else:
            await message.reply("Invalid format. Use /add_line <key> <value>")
    else:
        await message.reply("Please provide a key and a value. Example: /add_line key Smth")
