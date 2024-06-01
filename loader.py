from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from github import Github
from pyrogram import Client

from data import config
from data.config import GITHUB_TOKEN, GITHUB_REPO, BOT_TOKEN, API_ID, API_HASH
from filters.is_admin import AdminFilter

default=DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=config.BOT_TOKEN, default=default)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

is_admin_filter = AdminFilter(bot)

github = Github(GITHUB_TOKEN)
repository = github.get_user().get_repo(GITHUB_REPO)

app = Client(
        "Pyro Bot",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH
    )
