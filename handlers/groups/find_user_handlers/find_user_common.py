import asyncio
import random
from datetime import date

from aiogram.types import Message

from loader import pyro_client, main_bot
from utils.data.bot_data import BotData
from utils.data.group_data import SpecificChatData
from utils.data.user_data import UserData
from utils.misc.common import create_user_mention


async def send_typing_messages(chat_id, messages):
    for text, delay in messages:
        await main_bot.send_message(chat_id, text)
        await asyncio.sleep(delay)


async def detect_template(chat_id: int, title: str, data_selector, increment, skip_if_exist: bool = False):
    today = str(date.today())
    group_data = SpecificChatData.load(chat_id)

    data_set: dict = data_selector(group_data)

    if today in data_set:
        if skip_if_exist:
            return

        if group_data.debug:
            await main_bot.send_message(chat_id, f"Игнорируем предыдущий результат отладкой", parse_mode="Markdown")
        else:
            user_mention = create_user_mention(await main_bot.get_chat_member(chat_id, data_set[today]))
            await main_bot.send_message(chat_id, f"Сегодняшний ({today}) {title} уже определён! Это {user_mention}",
                                        parse_mode="Markdown")

            return

    users = group_data.users

    all_in_chat = await group_data.get_all_unmarked_users(today)

    if len(all_in_chat) == 0:
        if not group_data.aggressive_selection and len(group_data.registered_users) == 0:
            await main_bot.send_message(chat_id, "Aggressive mode is off and no one is registered!")
            return
        await main_bot.send_message(chat_id, "We have no one to choose from!")
        return

    group_data.locks[title] = True

    possible_messages = BotData.load().get_lines(group_data.lines_key)

    if len(possible_messages) < 5:
        for i in range(5 - len(possible_messages)):
            if len(possible_messages) == 0:
                possible_messages.append("NULL!!!")
                continue

            possible_messages.append(possible_messages[-1])

    selected_messages = random.sample(possible_messages, 4)
    messages = [(msg, group_data.delay) for msg in selected_messages]
    messages.append((f"Всё, теперь очевидно. Сегодня {title}...", 1))

    await send_typing_messages(chat_id, messages)

    random_user = random.choice(all_in_chat)
    user_id = str(random_user.user.id)

    data_set[today] = user_id
    user_data = users.get(user_id, UserData(user_id))
    users[user_id] = user_data
    increment(group_data, user_data, data_set)

    await main_bot.send_message(chat_id,
                                f"Это {create_user_mention(await main_bot.get_chat_member(chat_id, user_id))}!",
                                parse_mode="Markdown")

    group_data.save()
    group_data.locks[title] = False


async def detect_stats_template(message: Message, title: str, selector):
    chat_id = message.chat.id
    group_data = SpecificChatData.load(chat_id)

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
