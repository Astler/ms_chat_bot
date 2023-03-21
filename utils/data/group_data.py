import os

from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_json
from cat.utils.git_utils import get_cached_git, push_git_data


class GroupInfo(Serializable):
    users = {}
    pidors = {}
    heroes = {}

    @staticmethod
    def from_json(json_dct: dict):
        info = GroupInfo()

        info.users = json_dct.get("users", info.users)
        info.heroes = json_dct.get("heroes", info.heroes)
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
