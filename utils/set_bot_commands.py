from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("handsome", "Красавчик дня"),
        types.BotCommand("pidor", "Пидор дня"),
        types.BotCommand("handsome_stats", "Статистика красавчиков"),
        types.BotCommand("pidor_stats", "Статистика пидоров"),
    ])
