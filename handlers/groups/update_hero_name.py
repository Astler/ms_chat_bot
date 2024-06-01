from aiogram import types
from aiogram.filters import Command

from loader import dp, bot, is_admin_filter
from utils.data.group_data import save_group_data, get_group_data


@dp.message(Command(commands=["edit_hero_name", "set_hero_name"]), is_admin_filter)
async def hero_of_the_day(message: types.Message, command: Command):
    new_name = command.args

    if not new_name:
        await bot.send_message(message.chat.id, "Так не сработает. Введите имя сразу после команды в формате: "
                                                "/set_hero_name Новое имя")
        return

    chat_id = message.chat.id

    group_info = get_group_data(chat_id)

    if message.chat.title == new_name:
        await bot.send_message(message.chat.id, "Ничего не изменилось")
    else:
        group_info.hero_name = new_name
        await bot.send_message(message.chat.id, f"Меняю имя для \"Героя дня\" на \"{new_name}\"")

    save_group_data(chat_id, group_info)