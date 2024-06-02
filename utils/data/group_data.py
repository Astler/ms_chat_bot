from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_json
from cat.utils.git_utils import get_cached_git, push_git_data
from utils.data.user_data import UserData


class GroupInfo(Serializable):
    users = {}
    pidors = {}
    anime_guys = {}
    handsome_mens = {}

    def to_json(self):
        users = {}

        for user_id, user_obj in self.users.items():
            users[user_id] = user_obj.to_json_str()

        print(users)

        json_dict = self.__dict__.copy()
        json_dict["users"] = users

        return json_dict

    @staticmethod
    def from_json(json_dct: dict):
        info = GroupInfo()

        raw_users: dict = json_dct.get("users", info.users)
        print(raw_users)
        users = {}

        for raw_user_id, data in raw_users.items():
            print(data)
            user = UserData.from_json_str(data)
            users[str(raw_user_id)] = user

        info.users = users
        info.handsome_mens = json_dct.get("handsome_mens", info.handsome_mens)
        info.anime_guys = json_dct.get("anime_guys", info.anime_guys)
        info.pidors = json_dct.get("pidors", info.pidors)

        return info


def get_group_file(group_id: int):
    return f"product_groups/{group_id}.json"


def get_group_data(group_id: int) -> GroupInfo:
    return get_cached_git(get_group_file(group_id), GroupInfo())


def save_group_data(group_id: int, group_info: GroupInfo):
    path_file = get_group_file(group_id)

    save_local_json(path_file, group_info)
    push_git_data(path_file, group_info)
