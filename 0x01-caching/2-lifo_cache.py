#!/usr/bin/env python3
""" LIFO Caching """
BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache class definition
    """
    def __init__(self) -> None:
        super().__init__()

    def put(self, key, item) -> None:
        """
        Assign to the dictionary self.cache_data,
        the item value for the key
        """
        if key is None or item is None:
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_key = list(self.cache_data)[-1]
            del self.cache_data[first_key]
            print("DISCARD: {}".format(first_key))
        self.cache_data.update({key: item})

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        return self.cache_data.get(key, None)
