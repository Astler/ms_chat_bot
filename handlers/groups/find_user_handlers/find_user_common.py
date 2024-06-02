import asyncio
import random
from datetime import date

from aiogram.types import Message

from loader import pyro_client, main_bot
from utils.data.group_data import save_group_data, get_group_data
from utils.data.user_data import UserData
from utils.misc.common import create_user_mention
from utils.misc.resources import possible_messages


async def get_non_bot_chat_members(chat_id):
    non_bot_members = []
    async for member in pyro_client.get_chat_members(chat_id):
        if not member.user.is_bot:
            non_bot_members.append(member)
    return non_bot_members


async def send_typing_messages(chat_id, messages):
    for text, delay in messages:
        await main_bot.send_message(chat_id, text)
        await asyncio.sleep(delay)


async def get_all_unmarked_users(today, group_data, chat_id) -> list:
    all_in_chat = await get_non_bot_chat_members(chat_id)

    handsome_mens = group_data.handsome_mens
    if today in handsome_mens:
        for member in all_in_chat:
            if member.user.id.__eq__(handsome_mens[today]):
                all_in_chat.remove(member)

    pidors = group_data.pidors
    if today in pidors:
        for member in all_in_chat:
            if member.user.id.__eq__(pidors[today]):
                all_in_chat.remove(member)

    anime_guys = group_data.anime_guys
    if today in anime_guys:
        for member in all_in_chat:
            if member.user.id.__eq__(anime_guys[today]):
                all_in_chat.remove(member)

    return all_in_chat


async def detect_template(chat_id: int, title: str, data_set: dict, increment, callback, skip_if_exist: bool = False):
    group_data = get_group_data(chat_id)
    today = str(date.today())

    if today in data_set:
        if skip_if_exist:
            return

        user_mention = create_user_mention(await main_bot.get_chat_member(chat_id, data_set[today]))
        await main_bot.send_message(chat_id, f"Сегодняшний ({today}) {title} уже определён! Это {user_mention}",
                                    parse_mode="Markdown")

        return

    users = group_data.users

    all_in_chat = await get_all_unmarked_users(today, group_data, chat_id)

    if len(all_in_chat) == 0:
        await main_bot.send_message(chat_id, "Сегодня без титула никто не остался!")
        return

    selected_messages = random.sample(possible_messages, 4)
    messages = [(msg, 1) for msg in selected_messages]
    messages.append((f"Всё, теперь очевидно. Сегодня {title}...", 1))

    await send_typing_messages(chat_id, messages)

    random_user = random.choice(all_in_chat)
    user_id = str(random_user.user.id)

    data_set[today] = user_id

    user_data = users.get(user_id, UserData(user_id))
    increment(user_data)
    users[user_id] = user_data

    await main_bot.send_message(chat_id,
                                f"Это {create_user_mention(await main_bot.get_chat_member(chat_id, user_id))}!",
                                parse_mode="Markdown")

    group_data.users = users
    callback(data_set)

    save_group_data(chat_id, group_data)


async def detect_stats_template(message: Message, title: str, selector):
    chat_id = message.chat.id

    group_data = get_group_data(chat_id)

    if len(group_data.users) == 0:
        await message.reply(f"Таких пока нет!", parse_mode="Markdown")
        return

    sorted_users = sorted(group_data.users.items(), key=lambda x: selector(x[1]), reverse=True)

    stats = []

    place_emoji = ["🥇", "🥈", "🥉"]

    for index, (user_id, user_data) in enumerate(sorted_users):
        try:
            member = await pyro_client.get_chat_member(int(chat_id), int(user_id))
        except Exception as e:
            print(f"Error: PeerIdInvalid for user_id: {user_id}, chat_id: {chat_id}\n {e}")
            continue

        if not member.user.is_bot:
            place = place_emoji[index] if index < len(place_emoji) else f"{index + 1}."
            stats.append(f"{place} {create_user_mention(member)} был {title} {selector(user_data)} раз(а)")

    stats = "Расклад такой: \n\n" + "\n".join(stats)

    await message.reply(stats, parse_mode="Markdown")
