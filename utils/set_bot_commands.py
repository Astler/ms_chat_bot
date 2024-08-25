from aiogram.types import BotCommand

from loader import main_bot


async def set_default_commands():
    await main_bot.set_my_commands([
        BotCommand(command="all", description="ABROAD!"),
        BotCommand(command="p", description="πdor"),
        BotCommand(command="h", description="Handsome"),
        BotCommand(command="a", description="Anime"),
        BotCommand(command="hs", description="Handsome stats"),
        BotCommand(command="ps", description="π stats"),
        BotCommand(command="ass", description="Anime stats"),
    ])
