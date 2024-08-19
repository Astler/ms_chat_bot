import asyncio
import datetime
import logging
import sys

from data.config import TRIGGER_HOURS
from loader import *
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.groups.find_user_handlers.pidor_handlers.pidor import detect_pidor, pidor_router
from utils import on_startup_notify
from utils.data.bot_data import BotData
from utils.set_bot_commands import set_default_commands


async def on_startup():
    logging.info(main_dispatcher)

    await set_default_commands()
    await on_startup_notify(main_dispatcher)
    start_scheduler()


async def combined_print():
    print("combined_print")
    bot_data = BotData.load()
    for chatId in bot_data.chats_to_notify:
        try:
            await detect_pidor(chatId, skip_if_exist=True)
            await main_bot.send_message(chatId, "Morning sunshine! 🌞")
        except Exception as e:
            logging.error(f"Error occurred while sending morning message to chat {chatId}: {e}")


def start_scheduler():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        combined_print,
        CronTrigger(hour=TRIGGER_HOURS),
        id="morning_job",
        max_instances=1,
        replace_existing=True
    )

    scheduler.add_job(
        combined_print,
        CronTrigger(hour=TRIGGER_HOURS, minute=1),
        id="morning_job_backup",
        max_instances=1,
        replace_existing=True
    )

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Scheduler started at server time: {current_time}")
    scheduler.start()


async def on_shutdown(dp):
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)

    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning("Bot down")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    main_dispatcher.startup.register(on_startup)

    from handlers.groups.auto import auto_router
    from handlers.groups.debug import debug_router
    from handlers.groups.lines import lines_router
    from handlers.groups.group_id import tech_router
    from handlers.private.private_help import help_router
    from handlers.private.private_id import id_router
    from handlers.groups.all_call import all_router
    from handlers.groups.register import register_router
    from handlers.groups.find_user_handlers.anime_handlers.anime import anime_router
    from handlers.groups.find_user_handlers.handsome_handlers.handsome import handsome_router
    main_dispatcher.include_routers(
        main_router,
        auto_router,
        tech_router,
        handsome_router,
        pidor_router,
        all_router,
        debug_router,
        lines_router,
        anime_router,
        register_router,
        help_router,
        id_router
    )

    await pyro_client.start()
    await main_dispatcher.start_polling(main_bot)


if __name__ == "__main__":
    asyncio.run(main())
