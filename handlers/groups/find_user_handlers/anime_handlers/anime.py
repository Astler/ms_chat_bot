from aiogram import types, Router
from aiogram.filters import Command

from handlers.groups.find_user_handlers.find_user_common import detect_template, detect_stats_template
from utils.data.group_data import get_group_data, save_group_data

anime_router = Router()


@anime_router.message(Command(commands=["anime", "a"]))
async def anime(message: types.Message):
    await detect_anime(message.chat.id)


async def detect_anime(chat_id: int, skip_if_exist: bool = False):
    group_data = get_group_data(chat_id)

    print(chat_id)

    def increment(user, anime_guys):
        user.increment_anime_counter()
        group_data.anime_guys = anime_guys
        save_group_data(chat_id, group_data)

    await detect_template(chat_id, "анимешник", group_data, group_data.anime_guys, increment, skip_if_exist)


@anime_router.message(Command(commands=["anime_stats", "as"]))
async def anime_stats(message: types.Message):
    def selector(user):
        return user.anime_times

    await detect_stats_template(message, "анимешником", selector)
