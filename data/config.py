import os

from dotenv import load_dotenv

load_dotenv()

SECRET_AI=os.environ.get("AI")

BOT_TOKEN = os.environ.get("TOKEN_KEY")

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN_KEY")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
A_PATH = os.environ.get('A_PATH')

FTP_URL = os.environ.get('FTP_URL')
FTP_USER = os.environ.get('FTP_USER')
FTP_PASS = os.environ.get('FTP_PASS')

BANNERS_MAP_FILE = os.environ.get('BANNERS_MAP_FILE')
BE_VERSIONS_FILE = os.environ.get('BE_VERSIONS_FILE')
APPS_DATA_ROOT_URL = os.environ.get('APPS_DATA_ROOT_URL')

BOT_NAMES = "Bot|Бот|bot|бот".split("|")
######
# FB #
######

CERT_PATH = os.environ.get('CERT_PATH')
PROJECT_ID = os.environ.get('PROJECT_ID')
TRIGGER_HOURS = int(os.environ.get('TRIGGER_HOURS'))

if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN ' + str(BOT_TOKEN) + '?')
    quit()

WEBHOOK_HOST = f'https://catassistantbot.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 0

if not str(os.environ.get('PORT')).__contains__("None"):
    WEBAPP_PORT = os.environ.get('PORT', default=8000)


version = "1.0.0"