from aiogram import types, Router
from aiogram.filters import Command

from handlers.groups.find_user_handlers.find_user_common import detect_template, detect_stats_template
from utils.data.group_data import get_group_data

pidor_router = Router()


@pidor_router.message(Command(commands=["pidor", "p"]))
async def pidor(message: types.Message):
    await detect_pidor(message.chat.id)


async def detect_pidor(chat_id: int, skip_if_exist: bool = False):
    group_data = get_group_data(chat_id)

    def increment(user):
        user.increment_pidor_counter()

    await detect_template(chat_id, "пидор", group_data.pidors, increment, skip_if_exist)


@pidor_router.message(Command(commands=["pidor_stats", "ps"]))
async def pidor_stats(message: types.Message):
    def selector(user):
        return user.pidor_times

    await detect_stats_template(message, "пидором", selector)
