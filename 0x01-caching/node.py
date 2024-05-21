#!/usr/bin/python3
""" Node class """


class Node:
    """ Node class definition """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        """String representation"""
        return self.value
