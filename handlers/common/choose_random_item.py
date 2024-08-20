import random
import re

from aiogram import types, Router

from data.config import BOT_NAMES
from filters.or_filter import RandomItemFilter

random_router = Router()

@random_router.message(RandomItemFilter())
async def bot_choose(message: types.Message):
    msg_text = str(message.text).replace("?", "")

    pattern = r'^\s*(?:' + '|'.join(re.escape(name) for name in BOT_NAMES) + r')\s*,?\s*'
    msg_text = re.sub(pattern, '', msg_text, flags=re.IGNORECASE)

    variants = re.split(r'\s+или\s+', msg_text.strip())

    await message.reply(f"{random.choice(variants)}")
