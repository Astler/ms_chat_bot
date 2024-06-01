from loader import dp, bot, app
import asyncio


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


async def get_all_unmarked_users(today, group_data, chat_id) -> list:
    all_in_chat = await get_non_bot_chat_members(chat_id)

    handsome_mens = group_data.handsome_mens
    if today in handsome_mens:
        for member in all_in_chat:
            if member.user.id == handsome_mens[today]:
                all_in_chat.remove(member)

    pidors = group_data.pidors
    if today in pidors:
        for member in all_in_chat:
            if member.user.id == pidors[today]:
                all_in_chat.remove(member)

    return all_in_chat
