from aiogram import types, Router
from aiogram.filters import CommandObject, Command

from data.to_export import my_id
from filters import IsGroup
from filters.is_specific_user import IsSpecificUser
from utils.data.group_data import SpecificChatData

debug_router = Router()


@debug_router.message(IsGroup(), IsSpecificUser(my_id), Command(commands=["debug"]))
async def debug_command(message: types.Message, command: CommandObject):
    chat_id = message.chat.id
    group_data = SpecificChatData.load(chat_id)

    if command.args:
        action = command.args.lower()

        if action == "true":
            group_data.debug = True
            await message.reply("Now bot in debug mode")
            group_data.save()
        elif action == "false":
            group_data.debug = False
            await message.reply("Now bot NOT in debug mode")
            group_data.save()
        else:
            await message.reply("Invalid value. Use 'true' or 'false'.")
    else:
        await message.reply("Please provide a value: 'true' or 'false'.")



@debug_router.message(IsGroup(), IsSpecificUser(my_id), Command(commands=["morning_test"]))
async def debug_command(message: types.Message, command: CommandObject):
    chat_id = message.chat.id
    from boot import morning_message
    await morning_message(chat_id)

