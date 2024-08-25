from aiogram import types, Router
from aiogram.filters import Command

from filters import IsPrivate
from utils.misc import rate_limit

help_router = Router()


@rate_limit()
@help_router.message(Command("help"), IsPrivate())
async def bot_help(message: types.Message):
    text = [
        '\nPrivate Messages Interactions'
        '\n• Send sticker to get it ids'
        '\n'
        '\nPrivate Commands'
        '\n/id - Shows your telegram id'
        '\n'
        '\nCommon Messages Interactions'
        '\n• Random option with Or'
        '\n• Nikita mention'
        '\n• Random stickers from good sets (do not works in private messages)'
        '\n'
        '\nCommon Commands'
        '\n/ai *message* - Send message to AI (gpt-3.5-turbo)'
        '\n'
        '\nGroup Commands'
        '\n/call /all - Mention all users in chat'
        '\n'
        '\nSelection Commands'
        '\n/join - Join to selection'
        '\n/joined - Show all joined users'
        '\n/leave - Leave selection'
        '\n'
        '\n/pidor /p - Select pidor'
        '\n/anime /a - Select anime guy'
        '\n/handsome /h - Select handsome guy'
        '\n/pidor_stats /ps - Show pidor stats'
        '\n/anime_stats /as /ass - Show anime stats'
        '\n/handsome_stats /hs - Show handsome stats'
        '\n'
        '\nBot Settings (only admins)'
        '\n/chat_id - Shows chat id'
        '\n/lines *pack name* - Changes lines massive that can be used during selection'
        '\n/add_line *pack name* *line* - Adds new line to specific massive'
        '\n/aggressive_selection (true|false) - Affects selection logic, if active bot can select any user in chat as a target for selectors. If not - it can select only joined users.'
        '\n/debug (true|false) - Debug mode.'
        '\n/auto (true|false) - Daily auto trigger for /p /h and /a'
    ]

    formatted_text = '\n'.join(text)

    await message.answer(formatted_text)
