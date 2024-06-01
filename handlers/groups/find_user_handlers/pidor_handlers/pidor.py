import random
from datetime import date

from aiogram import types
from aiogram.filters import Command

from handlers.groups.find_user_handlers.find_user_common import send_typing_messages, \
    get_all_unmarked_users
from loader import dp, bot
from utils.data.group_data import save_group_data, get_group_data
from utils.data.user_data import UserData
from utils.misc.common import create_user_mention
from utils.misc.resources import possible_messages


@dp.message(Command(commands=["pidor", "p"]))
async def pidor(message: types.Message):
    await detect_pidor(message.chat.id)


async def detect_pidor(chat_id: int, skip_if_exist: bool = False):
    group_data = get_group_data(chat_id)
    pidors = group_data.pidors
    today = str(date.today())

    if today in pidors:
        if skip_if_exist:
            return

        user_mention = create_user_mention(await bot.get_chat_member(chat_id, pidors[today]))
        await bot.send_message(chat_id, f"Сегодняшний ({today}) пидор уже определён! Это {user_mention}",
                               parse_mode="Markdown")

        return

    users = group_data.users

    all_in_chat = await get_all_unmarked_users(today, group_data, chat_id)
    selected_messages = random.sample(possible_messages, 4)
    messages = [(msg, 1) for msg in selected_messages]
    messages.append(("Всё, теперь очевидно. Сегодня пидор...", 1))

    await send_typing_messages(chat_id, messages)

    random_user = random.choice(all_in_chat)
    user_id = str(random_user.user.id)

    pidors[today] = user_id

    user_data = users.get(user_id, UserData(user_id))
    user_data.increment_pidor_counter()
    users[user_id] = user_data

    await bot.send_message(chat_id,
                           f"Это {create_user_mention(await bot.get_chat_member(chat_id, user_id))}!",
                           parse_mode="Markdown")

    group_data.users = users
    group_data.pidors = pidors

    save_group_data(chat_id, group_data)
