from aiogram import types
from aiogram.filters import Command

from loader import dp, app
from utils.data.group_data import get_group_data
from utils.misc.common import create_user_mention


@dp.message(Command(commands=["pidor_stats", "ps"]))
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

