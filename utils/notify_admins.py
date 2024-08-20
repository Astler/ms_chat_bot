import logging

from aiogram import Dispatcher
from data.config import version
from utils.admin_data.data import get_a_list


async def on_startup_notify(dp: Dispatcher):
    await send_msg_to_admin(f"Бот продуктов запущен и готов к работе v{version}!")


async def on_shutdown_notify(dp: Dispatcher):
    await send_msg_to_admin("Работа бота завершена!")


async def send_msg_to_admin(msg: str):
    logging.error(msg)

    for admin in get_a_list():
        try:
            from loader import main_bot
            await main_bot.send_message(admin, msg)
        except Exception as err:
            logging.exception(err)
