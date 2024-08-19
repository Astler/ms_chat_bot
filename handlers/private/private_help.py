from aiogram import types, Router
from aiogram.filters import Command

from filters import IsPrivate
from utils.misc import rate_limit

help_router = Router()


@rate_limit()
@help_router.message(Command("help"), IsPrivate())
async def bot_help(message: types.Message):
    text = [
        'GROUPS ONLY',
        '/start - Инициализация бота с его добавлением в автоматический список',
        '/stop - Удаление бота из автосписка',
        '',
        '/members - Создаёт сообщение-призыв отметив всех в чате',
        '/abroad - Читай members',
        '',
        '/ps - Статистика по пидорам',
        '/p - Поиск пидора',
        '',
        '/hs - Статистика по красавчикам',
        '/h - Поиск красавчика',
        '',
        '',
        'Технические',
        '/chat_id - Отображает айди этого чата',
        '/id - бот вернет ваш id в TG (только в ЛС!)'
        '/sticker_id - тул для получения айди стикеров (только в ЛС!)'
    ]

    formatted_text = '\n'.join(text)

    await message.answer(formatted_text)
