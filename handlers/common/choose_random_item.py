import random

from aiogram import types

from filters.random_item_filter import RandomItemFilter
from loader import dp


@dp.message(RandomItemFilter())
async def bot_choose(message: types.Message):
    msg_text = str(message.text).replace("?", "")[3:].strip()

    if msg_text.startswith(","):
        msg_text = msg_text[2:]

    variants = msg_text.strip().split(" или ")

    await message.reply(f"{random.choice(variants)}")
