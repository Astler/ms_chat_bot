from aiogram import types
from aiogram.filters import BaseFilter


class RandomItemFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text.lower().startswith("бот") and " или " in message.text.lower()
