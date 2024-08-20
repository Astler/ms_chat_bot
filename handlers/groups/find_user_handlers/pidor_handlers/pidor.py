from aiogram import types, Router
from aiogram.filters import Command

from handlers.groups.find_user_handlers.find_user_common import detect_template, detect_stats_template

pidor_router = Router()


@pidor_router.message(Command(commands=["pidor", "p"]))
async def pidor(message: types.Message):
    await detect_pidor(message.chat.id)


async def detect_pidor(chat_id: int, skip_if_exist: bool = False, on_completed = None):
    def increment(group_data, user, pidors):
        user.increment_pidor_counter()
        group_data.pidors = pidors

    def data_selector(group_data):
        return group_data.pidors

    await detect_template(chat_id, "пидор", data_selector, increment, skip_if_exist)

    if on_completed is not None:
        await on_completed()

@pidor_router.message(Command(commands=["pidor_stats", "ps"]))
async def pidor_stats(message: types.Message):
    def selector(user):
        return user.pidor_times

    await detect_stats_template(message, "пидором", selector)
