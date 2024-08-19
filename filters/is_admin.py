from aiogram import types, Bot
from aiogram.enums import ChatType, ChatMemberStatus
from aiogram.filters import BaseFilter

from data.to_export import my_id


class AdminFilter(BaseFilter):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(self, message: types.Message) -> bool:
        if message.from_user.id == my_id:
            return True

        if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
            return False
        member = await self.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]
