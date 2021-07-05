from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import myChats


class MyChatFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return myChats.__contains__(message.chat.id)