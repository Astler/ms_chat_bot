import random
import re

import openai
from aiogram import types, Router
from aiogram.filters import Command, CommandObject

from data.config import BOT_NAMES
from filters.or_filter import RandomItemFilter
from loader import client
from utils.data.group_data import SpecificChatData

random_router = Router()
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

@random_router.message(RandomItemFilter())
async def bot_choose(message: types.Message):
    msg_text = str(message.text).replace("?", "")

    pattern = r'^\s*(?:' + '|'.join(re.escape(name) for name in BOT_NAMES) + r')\s*,?\s*'
    msg_text = re.sub(pattern, '', msg_text, flags=re.IGNORECASE)

    variants = re.split(r'\s+или\s+', msg_text.strip())

    await message.reply(f"{random.choice(variants)}")


@random_router.message(Command(commands=["ai"]))
async def bot_ai(message: types.Message, command: CommandObject):
    chat_id = message.chat.id
    group_data = SpecificChatData.load(chat_id)

    if command.args:
        user_message = command.args
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            ai_response = response.choices[0].message.content
            await message.reply(ai_response)
        except Exception as e:
            await message.reply(f"An error occurred: {str(e)}")
    else:
        await message.reply("Please provide a message after the /ai command.")