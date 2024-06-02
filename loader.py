from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from github import Github
from pyrogram import Client

from data import config
from filters.is_admin import AdminFilter

github = Github(config.GITHUB_TOKEN)
repository = github.get_user().get_repo(config.GITHUB_REPO)

default = DefaultBotProperties(parse_mode=ParseMode.HTML)
main_bot = Bot(token=config.BOT_TOKEN, default=default)
is_admin_filter = AdminFilter(main_bot)

pyro_client = Client(
    "Pyro Bot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

storage = MemoryStorage()
main_dispatcher = Dispatcher(storage=storage)
main_router = Router()
