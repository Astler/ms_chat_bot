from json import JSONEncoder


class UserInfo:
    pidor_times = 0
    hero_times = 0
    tg_id = ""

    def to_json(self):
        return self.__dict__

    def __init__(self, user_id=0):
        self.tg_id = user_id

    @staticmethod
    def from_json(json_dct: dict):
        info = UserInfo()

        info.pidor_times = json_dct.get("pidor_times", info.pidor_times)
        info.hero_times = json_dct.get("hero_times", info.hero_times)
        info.tg_id = json_dct.get("tg_id", info.tg_id)

        return info

    def increment_pidor_counter(self):
        self.pidor_times += 1
        return self

    class UserEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
