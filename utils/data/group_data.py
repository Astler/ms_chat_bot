from datetime import date

from cat.json.serializable import Serializable
from cat.utils.files_utils import save_local_json
from cat.utils.git_utils import get_cached_git, push_git_data
from data.to_export import bot_folder
from loader import cached_groups
from utils.data.user_data import UserData


def get_group_file(group_id: int):
    return f"{bot_folder}/{group_id}.json"


class SpecificChatData(Serializable):

    @staticmethod
    def instance(json_dct: dict):
        return SpecificChatData(json_dct["chat_id"])

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.debug = False
        self.delay = 2
        self.last_auto_day = ""
        self.aggressive_selection = False
        self.registered_users = []
        self.locks = {}

        self.users = {}
        self.pidors = {}
        self.lines_key = "default"
        self.anime_guys = {}
        self.handsome_mens = {}

    def to_json(self):
        users = {}

        for user_id, user_obj in self.users.items():
            users[user_id] = user_obj.to_json_str()

        json_dict = self.__dict__.copy()
        json_dict["users"] = users

        return json_dict

    def save(self):
        path_file = get_group_file(self.chat_id)

        save_local_json(path_file, self)
        push_git_data(path_file, self)

    async def get_all_unmarked_users(self, today) -> list:
        all_available_users_in_chat = await self.get_available_non_bot_chat_members()

        if self.debug:
            return all_available_users_in_chat

        marked_users = set()

        if today in self.handsome_mens:
            marked_users.add(self.handsome_mens[today])

        if today in self.pidors:
            marked_users.add(self.pidors[today])

        if today in self.anime_guys:
            marked_users.add(self.anime_guys[today])

        unmarked_users = [member for member in all_available_users_in_chat if str(member.user.id) not in marked_users]

        return unmarked_users

    async def get_available_non_bot_chat_members(self):
        non_bot_members = []

        if self.aggressive_selection:
            try:
                from loader import pyro_client
                async for member in pyro_client.get_chat_members(int(self.chat_id)):
                    if not member.user.is_bot:
                        non_bot_members.append(member)
            except Exception as e:
                print(f"An error occurred while retrieving chat members: {e}")
        else:
            for user_id in self.registered_users:
                from loader import pyro_client
                member = await pyro_client.get_chat_member(int(self.chat_id), int(user_id))
                if not member.user.is_bot:
                    non_bot_members.append(member)

        return non_bot_members

    @staticmethod
    def from_json(json_dct: dict):
        info = SpecificChatData(json_dct["chat_id"])

        raw_users: dict = json_dct.get("users", info.users)
        users = {}

        for raw_user_id, data in raw_users.items():
            user = UserData.from_json_str(data)
            users[str(raw_user_id)] = user

        info.users = users
        info.handsome_mens = json_dct.get("handsome_mens", info.handsome_mens)
        info.anime_guys = json_dct.get("anime_guys", info.anime_guys)
        info.pidors = json_dct.get("pidors", info.pidors)
        info.lines_key = json_dct.get("lines_key", info.lines_key)
        info.debug = json_dct.get("debug", info.debug)
        info.aggressive_selection = json_dct.get("aggressive_selection", info.aggressive_selection)
        info.registered_users = json_dct.get("registered_users", info.registered_users)
        info.delay = json_dct.get("delay", info.delay)
        info.locks = json_dct.get("locks", info.locks)
        info.last_auto_day = json_dct.get("last_auto_day", info.last_auto_day)

        return info

    @staticmethod
    def load(chat_id: int) -> 'SpecificChatData':
        if chat_id in cached_groups:
            return cached_groups[chat_id]

        file = get_group_file(chat_id)
        group_data = get_cached_git(file, SpecificChatData.from_json_str, SpecificChatData.from_json, {"chat_id": chat_id})
        cached_groups[chat_id] = group_data
        return group_data

    def is_today_auto_performed(self):
        today = str(date.today())
        return self.last_auto_day == today

    def track_morning(self):
        self.last_auto_day = str(date.today())
