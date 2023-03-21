import asyncio
import json
import random
from datetime import date

from aiogram import types

from loader import dp, bot, app
from utils.data.group_data import save_group_data, get_group_data
from utils.group_data.data import get_user_info
from utils.misc.common import create_user_mention
from utils.user_data.user_info import UserInfo


async def get_non_bot_chat_members(chat_id):
    non_bot_members = []
    async for member in app.get_chat_members(chat_id):
        if not member.user.is_bot:
            non_bot_members.append(member)
    return non_bot_members


async def send_typing_messages(chat_id, messages):
    for text, delay in messages:
        await bot.send_message(chat_id, text)
        await asyncio.sleep(delay)


@dp.message_handler(commands=["pidor_stats", "ps"])
async def my_rep(message: types.Message):
    chat_id = message.chat.id

    group_data = get_group_data(chat_id)
    all_users = group_data.users

    stats = []

    for user_id in all_users:
        cat_user: UserInfo = json.loads(all_users[user_id], object_hook=lambda d: UserInfo(**d))
        try:
            member = await app.get_chat_member(chat_id, cat_user.tg_id)
            if not member.user.is_bot:
                stats.append(f"{create_user_mention(member)} был пидором {cat_user.pidor_times} раз")
        except Exception as e:
            print(f"exception {e}")

    await message.reply("\n".join(stats), parse_mode="Markdown")


@dp.message_handler(commands=["pidor", "p"])
async def my_rep(message: types.Message):
    chat_id = message.chat.id
    await detect_pidor(chat_id)


async def detect_pidor(chat_id: int):
    group_data = get_group_data(chat_id)
    all_in_chat = await get_non_bot_chat_members(chat_id)

    pidors = group_data.pidors
    users = group_data.users

    today = str(date.today())

    if today not in pidors:
        messages = [
            ("Провожу опрос общих знакомых", 1),
            ("Спрашиваю ваших родителей", 1),
            ("Задаю вопросы усопшим", 1),
            ("Иду к шаману", 1),
            ("Всё, теперь очевидно. Сегодня пидор...", 1)
        ]

        await send_typing_messages(chat_id, messages)

        random_user = random.choice(all_in_chat)
        user_id = random_user.user.id
        pidors[today] = user_id

        users[user_id] = json.dumps(get_user_info(users, user_id).increment_pidor_counter(), cls=UserInfo.UserEncoder)

        await bot.send_message(chat_id,
                               f"Это {create_user_mention(await bot.get_chat_member(chat_id, user_id))}!",
                               parse_mode="Markdown")
    else:
        user_id = pidors[today]
        await bot.send_message(chat_id,
                               f"Сегодняшний ({today}) пидор уже определён! Это {create_user_mention(await bot.get_chat_member(chat_id, user_id))}",
                               parse_mode="Markdown")

    group_data.users = users
    group_data.pidors = pidors

    save_group_data(chat_id, group_data)
