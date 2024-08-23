import random
import re

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import Sticker

from filters import IsPrivate
from utils.misc import rate_limit

id_router = Router()

GOOD_SETS = ['video_gachi', 'ukrgachimemes']
NIKITA = 'CAACAgIAAxkBAAIBH2bIegP8XT4sLEBH-PQYnvcUs39_AAJcUwACw5J5SCUKm-EflgGzNQQ'
NIKITA_PATTERN = re.compile(r'\b(никит|nickyt|никитос|никитк|никитушк)\w*', re.IGNORECASE)

@rate_limit()
@id_router.message(Command("id"), IsPrivate())
async def bot_help(message: types.Message):
    await message.answer(str(message.from_user.id))


@id_router.message(lambda message: message.sticker is not None)
async def handle_sticker(message: types.Message):
    sticker: Sticker = message.sticker
    if sticker.set_name in GOOD_SETS:
        sticker_set = await message.bot.get_sticker_set(sticker.set_name)
        random_sticker = random.choice(sticker_set.stickers)
        await message.answer_sticker(random_sticker.file_id)

@id_router.message(lambda message: message.text is not None)
async def handle_nikita_mention(message: types.Message):
    if NIKITA_PATTERN.search(message.text):
        await message.answer_sticker(NIKITA)