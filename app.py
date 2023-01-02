import asyncio
import logging
import os

import aioschedule as aioschedule

from data.config import (WEBHOOK_URL, WEBHOOK_PATH,
                         WEBAPP_HOST, WEBAPP_PORT)
from loader import bot, app
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)

    import filters
    filters.setup(dp)
    logging.info(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)

    async def noon_print():
        await dp.bot.send_message("-1001216924947", "TIME NOON!!!!")
        print("It's noon!")

    async def test_print():
        await dp.bot.send_message("-1001216924947", "Time!")
        print("Test print!")

    async def scheduler():
        aioschedule.every().day.at("12:00").do(noon_print)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)

    async def scheduler_test():
        aioschedule.every().minute.do(test_print)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)

    asyncio.create_task(scheduler())
    asyncio.create_task(scheduler_test())


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
