from aiogram import types, Router
from aiogram.filters import Command

from handlers.groups.find_user_handlers.find_user_common import detect_template, detect_stats_template

handsome_router = Router()


@handsome_router.message(Command(commands=["handsome", "h"]))
async def handsome(message: types.Message):
    await detect_handsome(message.chat.id)


async def detect_handsome(chat_id: int, skip_if_exist: bool = False):
    def increment(group_data, user, handsome_mens):
        user.increment_handsome_counter()
        group_data.handsome_mens = handsome_mens

    def data_selector(group_data):
        return group_data.handsome_mens

    await detect_template(chat_id, "красавчик", data_selector, increment, skip_if_exist)


@handsome_router.message(Command(commands=["handsome_stats", "hs"]))
async def anime_stats(message: types.Message):
    def selector(user):
        return user.handsome_times

    await detect_stats_template(message, "красавчиком", selector)
