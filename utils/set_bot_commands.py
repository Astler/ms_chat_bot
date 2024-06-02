from aiogram.types import BotCommand

from loader import main_bot


async def set_default_commands():
    await main_bot.set_my_commands([
        BotCommand(command="abroad", description="Все на борт!"),
        BotCommand(command="handsome", description="Красавчик дня"),
        BotCommand(command="pidor", description="Пидор дня"),
        BotCommand(command="handsome_stats", description="Статистика красавчиков"),
        BotCommand(command="pidor_stats", description="Статистика пидоров"),
    ])
