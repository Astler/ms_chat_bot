from aiogram import types, Router
from aiogram.filters import Command

from handlers.groups.find_user_handlers.find_user_common import detect_template, detect_stats_template
from utils.data.group_data import get_group_data

handsome_router = Router()


@handsome_router.message(Command(commands=["handsome", "h"]))
async def handsome(message: types.Message):
    await detect_handsome(message.chat.id)


async def detect_handsome(chat_id: int, skip_if_exist: bool = False):
    group_data = get_group_data(chat_id)

    def update_guys(handsome_mens):
        group_data.handsome_mens = handsome_mens

    def increment(user):
        user.increment_handsome_counter()

    await detect_template(chat_id, "красавчик", group_data.handsome_mens, increment, update_guys, skip_if_exist)


@handsome_router.message(Command(commands=["handsome_stats", "hs"]))
async def anime_stats(message: types.Message):
    def selector(user):
        return user.handsome_times

    await detect_stats_template(message, "красавчиком", selector)
