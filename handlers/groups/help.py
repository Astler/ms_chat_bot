from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit()
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'GROUPS ONLY',
        '/start - Инициализация бота с его добавлением в автоматический список',
        '/stop - Удаление бота из автосписка',
        '',
        '/members - Создаёт сообщение-призыв отметив всех в чате',
        '/abroad - Читай members',
        '',
        '/pidor_stats - Статистика по пидорам',
        '/ps - Читай pidor_stats',
        '',
        '/pidor - Поиск пидора',
        '/p - Читай pidor',
        '',
        '/handsome_stats - Статистика по красавчикам',
        '/hs - Читай handsome_stats',
        '',
        '/handsome - Поиск красавчика',
        '/h - Читай handsome',
        '',
        '/chat_id - Отображает айди этого чата',
        '',
        'Технические',
        '/id - бот вернет ваш id в TG (только в ЛС!)'
        '/sticker_id - тул для получения айди стикеров (только в ЛС!)'
    ]

    formatted_text = '\n'.join(text)

    await message.answer(formatted_text)
