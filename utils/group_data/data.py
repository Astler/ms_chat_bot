import json
import os

from github import GithubException

from loader import repository
from utils.group_data.group_info import GroupInfo
from utils.user_data.user_info import UserInfo


def get_user_info(users: dict, user_id: int) -> UserInfo:
    if users.__contains__(str(user_id)):
        user_json = users[str(user_id)]
        print(f"has user = {user_json}")
        return json.loads(user_json, object_hook=lambda d: UserInfo(**d))
    else:
        print(f"new user!!")
        return UserInfo(user_id)


def get_group_info(group_id: int) -> GroupInfo:
    if os.path.exists(get_local_file(group_id)):
        try:
            return get_local_dict(group_id)
        except Exception as e:
            print(e)
            return get_git_dict(group_id)
    else:
        return get_git_dict(group_id)


def save_group_dict(group_id: int, group_info: GroupInfo):
    file_name = get_git_group_file(group_id)

    try:
        contents = repository.get_contents(file_name)
        repository.update_file(file_name, "group file", json.dumps(group_info.to_json()), contents.sha)
    except GithubException:
        repository.create_file(file_name, "group file", json.dumps(group_info.to_json()))

    save_local_dict(group_id, group_info)

### LOCAL ###

def get_local_file(group_id: int):
    return os.getcwd() + f"/groups/{group_id}.json"


def get_local_dict(group_id: int):
    open(get_local_file(group_id), 'a').close()
    user_file = open(get_local_file(group_id), 'r')
    contents = user_file.read()
    user_file.close()

    if len(contents) != 0:
        group_data = json.loads(contents)
        return GroupInfo.from_json(group_data)
    else:
        empty_data = GroupInfo()
        save_local_dict(group_id, empty_data)
        return empty_data


def save_local_dict(group_id: int, group_info: GroupInfo):
    filename = get_local_file(group_id)

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            print(exc)

    with open(filename, 'w') as f:
        f.write(json.dumps(group_info.to_json()))


### GITHUB ###

def get_git_group_file(group_id: int):
    return f"product_groups/{group_id}.json"


def get_git_dict(group_id: int) -> GroupInfo:
    group_info = GroupInfo()

    try:
        file = repository.get_contents(get_git_group_file(group_id))

        contents = file.decoded_content.decode()

        if len(contents) != 0:
            group_info = GroupInfo.from_json(json.loads(contents))
        else:
            save_local_dict(group_id, group_info)

    except GithubException:
        save_group_dict(group_id, group_info)

    save_local_dict(group_id, group_info)

    return group_info
