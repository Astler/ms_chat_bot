from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_json
from cat.utils.git_utils import push_git_data, get_cached_git
from data.to_export import global_bot_settings_file
from utils.data.lines import default_lines, ms_lines


class BotData(Serializable):

    def __init__(self):
        self.chats_to_notify = []
        self.lines_keys = {"ms": ms_lines}

    def get_lines(self, key):
        if key in self.lines_keys:
            return self.lines_keys[key]

        return default_lines

    @staticmethod
    def load() -> 'BotData':
        return get_cached_git(global_bot_settings_file, BotData.from_json_str, BotData.from_json)

    @staticmethod
    def instance(json_dct: dict):
        return BotData()

    @staticmethod
    def from_json(json_dct: dict):
        info = BotData()
        info.chats_to_notify = json_dct.get("chats_to_notify", info.chats_to_notify)
        info.lines_keys = json_dct.get("lines_keys", info.lines_keys)
        return info

    def save(self):
        save_local_json(global_bot_settings_file, self)
        push_git_data(global_bot_settings_file, self)
