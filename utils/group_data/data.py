import json

from utils.user_data.user_info import UserInfo


def get_user_info(users: dict, user_id: int) -> UserInfo:
    if users.__contains__(str(user_id)):
        user_json = users[str(user_id)]
        print(f"has user = {user_json}")
        return json.loads(user_json, object_hook=lambda d: UserInfo(**d))
    else:
        print(f"new user!!")
        return UserInfo(user_id)

