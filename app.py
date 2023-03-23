import asyncio
import logging
import os
import datetime

import aioschedule as aioschedule
from aiogram.utils.exceptions import MigrateToChat
from data.config import (WEBHOOK_URL)
from handlers.groups.pidor import detect_pidor

from loader import bot, app
from utils.data.bot_data import get_bot_data
from utils.set_bot_commands import set_default_commands
from filters import setup as setup_filters
from utils.notify_admins import on_startup_notify


async def on_startup(dp):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)

    setup_filters(dp)
    logging.info(dp)

    await on_startup_notify(dp)
    await set_default_commands(dp)

    asyncio.ensure_future(scheduler_combined())


async def combined_print():
    now = datetime.datetime.now()
    bot_data = get_bot_data()

    if now.hour == 7 and now.minute == 0:
        for chatId in bot_data.chats_to_notify:
            print(f"chatId = {chatId}")
            await detect_pidor(chatId, skip_if_exist=True)
            await dp.bot.send_message(chatId, "TIME NOON!!!!")
        print("It's noon!")
    elif now.minute == 0:
        for chatId in bot_data.chats_to_notify:
            await send_message_to_chat_by_id(chatId, f"Hours ping {now.hour}")


async def send_message_to_chat_by_id(chat_id: int, message: str):
    try:
        await dp.bot.send_message(chat_id, message)
        print(f"ping chatId = {chat_id}")
    except MigrateToChat as e:
        new_chat_id = e.migrate_to_chat_id
        print(f"Group migrated to supergroup. Old chat ID: {chat_id}, New chat ID: {new_chat_id}")
        await dp.bot.send_message(new_chat_id, message)
        print(f"ping changed chatId = {new_chat_id}")


async def scheduler_combined():
    aioschedule.every().minute.do(combined_print)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)

    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning("Bot down")


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    path = os.getcwd() + "/users/"

    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    app.start()

    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup, on_shutdown=on_shutdown, )
