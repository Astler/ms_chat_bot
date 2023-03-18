import asyncio
import logging
import os
import datetime

import aioschedule as aioschedule

from data.config import (WEBHOOK_URL)

from loader import bot, app
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
    if now.hour == 12 and now.minute == 0:
        await dp.bot.send_message("-1001216924947", "TIME NOON!!!!")
        print("It's noon!")
    elif now.minute == 0:
        await dp.bot.send_message("-1001216924947", f"Hours ping {now.hour}")
    else:
        await dp.bot.send_message("-1001216924947", "Time!")
        print("Test print!")


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
