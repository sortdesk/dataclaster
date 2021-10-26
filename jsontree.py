from functools import reduce


class JSONTree:
    def __init__(self, dictionary: dict) -> None:
        self.dictionary = dictionary

    def recursive_get(self, keys: list):
        return reduce(lambda dic, key: dic.get(key), keys, self.dictionary)

    def get_value(self, path: str):
        keys = path.split(".")
        return self.recursive_get(keys)
