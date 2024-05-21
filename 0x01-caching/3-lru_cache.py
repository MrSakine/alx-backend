#!/usr/bin/env python3
""" LRUCache Caching """
BaseCaching = __import__("base_caching").BaseCaching
Node = __import__("node").Node


class LRUCache(BaseCaching):
    """
    LRUCache class definition
    """

    def __init__(self) -> None:
        super().__init__()
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        
    def _remove(self, node: Node):
        """Remove a node"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next, next_node.prev = next_node, prev_node
        
    def _add(self, node: Node):
        """Add a new node"""
        next_to_head = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_to_head
        next_to_head.prev = node

    def put(self, key, item) -> None:
        """
        Assign to the dictionary self.cache_data,
        the item value for the key
        """
        if key is None or item is None:
            return
        node = self.cache_data.get(key)
        if node:
            self._remove(node)
        new_node = Node(key, item)
        self.cache_data[key] = new_node
        self._add(new_node)
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache_data[lru.key]
            print("DISCARD: {}".format(lru.key))

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        node = self.cache_data.get(key)
        if not node:
            return None
        self._remove(node)
        self._add(node)
        return node.value
