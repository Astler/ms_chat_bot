from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_json
from cat.utils.git_utils import get_cached_git, push_git_data


class UserData(Serializable):
    pidor_times = 0
    handsome_times = 0
    tg_id = ""

    def __init__(self, user_id=0):
        self.tg_id = user_id

    @staticmethod
    def from_json(json_dct: dict):
        info = UserData()

        info.pidor_times = json_dct.get("pidor_times", info.pidor_times)
        info.handsome_times = json_dct.get("handsome_times", info.handsome_times)
        info.tg_id = json_dct.get("tg_id", info.tg_id)

        return info

    def increment_pidor_counter(self):
        self.pidor_times += 1
        return self

    def increment_handsome_counter(self):
        self.handsome_times += 1
        return self


def get_user_file(user_id: int):
    return f"users/{user_id}.json"


def get_user_data(group_id: int) -> UserData:
    return get_cached_git(get_user_file(group_id), UserData())


def save_user_data(user_id: int, user_info: UserData):
    path_file = get_user_file(user_id)

    save_local_json(path_file, user_info)
    push_git_data(path_file, user_info)
