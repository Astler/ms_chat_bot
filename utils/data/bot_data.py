from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_json
from cat.utils.git_utils import push_git_data, get_cached_git


class BotData(Serializable):

    def __init__(self):
        self.chats_to_notify = []

    @staticmethod
    def instance(json_dct: dict):
        return BotData()

    @staticmethod
    def from_json(json_dct: dict):
        info = BotData()
        info.chats_to_notify = json_dct.get("chats_to_notify", info.chats_to_notify)
        return info


def get_git_bot_data_file():
    return "product_bot_data.json"


def get_bot_data() -> BotData:
    return get_cached_git(get_git_bot_data_file(), BotData.from_json_str)


def save_bot_data(bot_data: BotData):
    file_name = get_git_bot_data_file()
    save_local_json(file_name, bot_data)
    push_git_data(file_name, bot_data)
