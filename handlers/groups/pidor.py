import asyncio
import random
from datetime import date

from aiogram import types
from aiogram.filters import Command

from loader import dp, bot, app
from utils.data.group_data import save_group_data, get_group_data
from utils.data.user_data import UserData
from utils.misc.common import create_user_mention
from utils.misc.resources import possible_messages


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


@dp.message(Command("pidor_stats"), Command("ps"))
async def pidor_stats(message: types.Message):
    chat_id = message.chat.id

    group_data = get_group_data(chat_id)

    if len(group_data.users) == 0:
        await message.reply("Никто не пидор, все красавчики!", parse_mode="Markdown")
        return

    sorted_users = sorted(group_data.users.items(), key=lambda x: x[1].pidor_times, reverse=True)

    stats = []

    place_emoji = ["🥇", "🥈", "🥉"]

    for index, (user_id, user_data) in enumerate(sorted_users):
        try:
            member = await app.get_chat_member(int(chat_id), int(user_id))
        except Exception as e:
            print(f"Error: PeerIdInvalid for user_id: {user_id}, chat_id: {chat_id}\n {e}")
            continue

        if not member.user.is_bot:
            place = place_emoji[index] if index < len(place_emoji) else f"{index + 1}."
            stats.append(f"{place} {create_user_mention(member)} был пидором {user_data.pidor_times} раз(а)")

    stats = "Расклад такой: \n\n" + "\n".join(stats)

    await message.reply(stats, parse_mode="Markdown")


@dp.message(Command("pidor"), Command("p"))
async def pidor(message: types.Message):
    await detect_pidor(message.chat.id)


async def detect_pidor(chat_id: int, skip_if_exist: bool = False):
    group_data = get_group_data(chat_id)

    pidors = group_data.pidors

    today = str(date.today())

    if today in pidors:
        if not skip_if_exist:
            print(pidors[today])
            user_mention = create_user_mention(await bot.get_chat_member(chat_id, pidors[today]))
            await bot.send_message(chat_id, f"Сегодняшний ({today}) пидор уже определён! Это {user_mention}",
                                   parse_mode="Markdown")

        return

    users = group_data.users

    all_in_chat = await get_non_bot_chat_members(chat_id)

    handsome_mens = group_data.handsome_mens
    if today in handsome_mens:
        for member in all_in_chat:
            if member.user.id == handsome_mens[today]:
                all_in_chat.remove(member)

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
