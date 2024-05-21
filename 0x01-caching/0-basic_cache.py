#!/usr/bin/env python3
""" Basic dictionary """
BaseCaching = __import__('main').BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class definition
    """
    def __init__(self) -> None:
        super().__init__()

    def put(self, key, item) -> None:
        """
        Set a new item into the cache through @key
        """
        if key is None or item is None:
            return
        self.cache_data.update({key: item})

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        return self.cache_data.get(key, None)
