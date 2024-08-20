from aiogram import types, Bot
from aiogram.filters import BaseFilter

from data.config import BOT_NAMES


class RandomItemFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        possible_names = (name.lower() for name in BOT_NAMES)
        message_text = message.text.lower()
        return any(message_text.startswith(name) for name in possible_names) and message_text.__contains__(" или ")
