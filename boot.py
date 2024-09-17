import asyncio
import datetime
import logging
import os
import random
import sys

from aiogram.types import FSInputFile

from data.config import TRIGGER_HOURS
from data.strings import glados_morning_messages
from handlers.common.ai_text_to_voice import text_to_voice
from handlers.groups.find_user_handlers.anime_handlers.anime import detect_anime
from handlers.groups.find_user_handlers.handsome_handlers.handsome import detect_handsome
from loader import *
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.groups.find_user_handlers.pidor_handlers.pidor import detect_pidor, pidor_router
from utils import on_startup_notify
from utils.data.bot_data import BotData
from utils.data.group_data import SpecificChatData
from utils.notify_admins import send_msg_to_admin
from utils.set_bot_commands import set_default_commands


async def on_startup():
    logging.info(main_dispatcher)

    await set_default_commands()
    await on_startup_notify(main_dispatcher)
    start_scheduler()


async def combined_print():
    bot_data = BotData.load()
    for chat_id in bot_data.chats_to_notify:
        await morning_message(chat_id)


async def morning_message(chat_id):
    try:
        group_data = SpecificChatData.load(chat_id)

        if group_data.is_today_auto_performed():
            return

        async def on_handsome_completed():
            await main_bot.send_message(chat_id, "Morning!")

            glados_message = random.choice(glados_morning_messages)

            audio_content = await text_to_voice(glados_message, "glados")

            if audio_content:
                with open("morning_message.mp3", "wb") as audio_file:
                    audio_file.write(audio_content)
                audio = FSInputFile("morning_message.mp3")
                await main_bot.send_voice(chat_id, audio)
                os.remove("morning_message.mp3")
            else:
                await main_bot.send_message(chat_id, glados_message)

        async def on_anime_completed():
            await detect_handsome(chat_id, skip_if_exist=True, on_completed=on_handsome_completed)

        async def on_pidor_completed():
            await detect_anime(chat_id, skip_if_exist=True, on_completed=on_anime_completed)

        await detect_pidor(chat_id, skip_if_exist=True, on_completed=on_pidor_completed)

        group_data.track_morning()
        group_data.save()
    except Exception as e:
        await send_msg_to_admin(msg=f"Error occurred while sending morning message to chat {chat_id}: {e}")


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

    from handlers.groups.aggressive_mode import aggressive_selection_router
    from handlers.groups.auto import auto_router
    from handlers.groups.debug import debug_router
    from handlers.groups.lines import lines_router
    from handlers.groups.group_id import tech_router
    from handlers.common.choose_random_item import random_router
    from handlers.common.ai_text_to_voice import text_to_voice_router
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
        aggressive_selection_router,
        all_router,
        debug_router,
        lines_router,
        anime_router,
        random_router,
        text_to_voice_router,
        register_router,
        help_router,
        id_router
    )

    await pyro_client.start()
    await main_dispatcher.start_polling(main_bot)


if __name__ == "__main__":
    asyncio.run(main())
