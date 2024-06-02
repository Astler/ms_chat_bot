from aiogram.types import BotCommand


async def set_default_commands(bot):
    await bot.set_my_commands([
        BotCommand("abroad", "Все на борт!"),
        BotCommand("handsome", "Красавчик дня"),
        BotCommand("pidor", "Пидор дня"),
        BotCommand("handsome_stats", "Статистика красавчиков"),
        BotCommand("pidor_stats", "Статистика пидоров"),
    ])
