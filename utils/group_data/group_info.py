class GroupInfo:
    users = {}
    pidors = {}
    heroes = {}

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_dct: dict):
        info = GroupInfo()

        info.users = json_dct.get("users", info.users)
        info.heroes = json_dct.get("heroes", info.heroes)
        info.pidors = json_dct.get("pidors", info.pidors)

        return info
