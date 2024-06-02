import json

from abc import ABC, abstractmethod


class Serializable(ABC):

    def to_json(self):
        return self.__dict__

    @staticmethod
    @abstractmethod
    def from_json(json_dct: dict):
        pass

    @staticmethod
    @abstractmethod
    def instance(json_dct: dict):
        pass

    def to_json_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_json_str(cls, json_str: str):
        if json_str is None or json_str is str and len(json_str) == 0:
            return cls.instance({})

        json_dct = json.loads(json_str)
        return cls.from_json(json_dct)
