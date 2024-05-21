#!/usr/bin/env python3
""" MRUCache Caching """
BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class definition
    """
    def __init__(self):
        super().__init__()
        self.recent_keys = []

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key in self.cache_data:
            self.recent_keys.remove(key)
            self.recent_keys.append(key)
            return self.cache_data[key]
        else:
            return None

    def put(self, key, value):
        """
        Assign to the dictionary self.cache_data,
        the item value for the key
        """
        if key in self.cache_data:
            self.recent_keys.remove(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                mru_key = self.recent_keys.pop()
                del self.cache_data[mru_key]
                print("DISCARD: {}".format(mru_key))
        self.cache_data[key] = value
        self.recent_keys.append(key)
