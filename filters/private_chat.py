from aiogram import types
from aiogram.enums import ChatType
from aiogram.filters import BaseFilter


class IsPrivate(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type == ChatType.PRIVATE
