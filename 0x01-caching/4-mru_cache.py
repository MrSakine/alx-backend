#!/usr/bin/env python3
""" MRUCache Caching """
from collections import OrderedDict
BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache class definition
    """
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key is not None and key in self.cache_data:
            self.cache_data.move_to_end(key, last=False)
        return self.cache_data.get(key, None)

    def put(self, key, item):
        """
        Assign to the dictionary self.cache_data,
        the item value for the key
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                mru_key = self.cache_data.popitem(False)[0]
                print("DISCARD: {}".format(mru_key))
            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=False)
        else:
            self.cache_data[key] = item
