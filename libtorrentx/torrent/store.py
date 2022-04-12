from contextlib import suppress
import ujson as json
import threading


class TorrentStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.__torrents = {}

    def contains(self, key):
        with self.lock:
            return key in self.__torrents

    def get(self, key):
        with self.lock:
            return self.__torrents.get(key, None)

    def add(self, key, value):
        with self.lock:
            self.__torrents[key] = value

    def remove(self, key):
        with self.lock:
            if key in self.__torrents:
                del self.__torrents[key]

    def all(self):
        return self.__torrents

    def __repr__(self):
        with self.lock:
            return str(self.__torrents)
