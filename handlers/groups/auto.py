from aiogram import types, Router
from aiogram.filters import CommandObject, Command

from filters import IsGroup
from loader import is_admin_filter
from utils.data.bot_data import BotData

auto_router = Router()


@auto_router.message(IsGroup(), is_admin_filter, Command(commands=["auto"]))
async def auto_command(message: types.Message, command: CommandObject):
    chat_id = message.chat.id
    bot_data = BotData.load()

    if command.args:
        action = command.args.lower()

        if action == "true":
            if chat_id in bot_data.chats_to_notify:
                await message.reply("Already in!")
            else:
                bot_data.chats_to_notify.append(chat_id)
                bot_data.save()
                await message.reply("Added to automatic commands list!")
        elif action == "false":
            if chat_id in bot_data.chats_to_notify:
                bot_data.chats_to_notify.remove(chat_id)
                bot_data.save()
                await message.reply("Removed chat from automatic operations!")
            else:
                await message.reply("Chat is not in auto commands list!")
        else:
            await message.reply("Invalid value. Use 'true' to add or 'false' to remove.")
    else:
        await message.reply("Please provide a value: 'true' to add or 'false' to remove.")

