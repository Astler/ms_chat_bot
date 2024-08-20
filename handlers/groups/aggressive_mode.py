from aiogram import types, Router
from aiogram.filters import CommandObject, Command

from data.to_export import my_id
from filters import IsGroup
from filters.is_specific_user import IsSpecificUser
from utils.data.group_data import SpecificChatData

aggressive_selection_router = Router()


@aggressive_selection_router.message(IsGroup(), IsSpecificUser(my_id), Command(commands=["aggressive_selection"]))
async def aggressive_selection_command(message: types.Message, command: CommandObject):
    chat_id = message.chat.id
    group_data = SpecificChatData.load(chat_id)

    if command.args:
        action = command.args.lower()

        if action == "true":
            group_data.aggressive_selection = True
            await message.reply("I'll decide for myself now")
            group_data.save()
        elif action == "false":
            group_data.aggressive_selection = False
            await message.reply("Well, fuck off")
            group_data.save()
        else:
            await message.reply("Invalid value. Use 'true' or 'false'.")
    else:
        await message.reply("Please provide a value: 'true' or 'false'.")

