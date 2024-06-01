from aiogram import types
from aiogram.enums import ChatType
from aiogram.filters import BaseFilter


class IsGroup(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)
