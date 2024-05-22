#!/usr/bin/env python3
""" LRUCache Caching """
BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache class definition
    """

    def __init__(self) -> None:
        super().__init__()
        self.__count = 0
        self.__keys = []
        self.__counts = []

    def put(self, key, item) -> None:
        """
        Assign to the dictionary self.cache_data,
        the item value for the key
        """
        if not key or not item:
            return
        if key in self.__keys:
            index = self.__keys.index(key)
            self.__keys.pop(index)
            self.__counts.pop(index)
        if len(self.__keys) == BaseCaching.MAX_ITEMS:
            index = self.__counts.index(min(self.__counts))
            self.__counts.pop(index)
            self.cache_data.pop(self.__keys[index])
            print('DISCARD: {}'.format(self.__keys.pop(index)))
        self.__keys.append(key)
        self.__counts.append(self.__count)
        self.cache_data.update({key: item})
        self.__count += 1

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key in self.__keys:
            self.__count += 1
            self.__counts[self.__keys.index(key)] = self.__count
        return self.cache_data.get(key)
