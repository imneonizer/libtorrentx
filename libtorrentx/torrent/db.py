import os
import threading
from contextlib import suppress
import ujson as json


class TorrentDB:
    def __init__(self, path="status.json"):
        self.lock = threading.Lock()
        self.path = path
        if not self.path.endswith(".json"):
            self.path = os.path.join(path, 'status.json')
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def eval(self, value):
        with suppress(Exception):
            return eval(value)
        return value

    def read(self):
        with self.lock:
            try:
                with open(self.path, 'r') as f:
                    return json.loads(f.read())
            except (FileNotFoundError, ValueError):
                return {}

    def write(self, data):
        with self.lock:
            with open(self.path, "w") as f:
                f.write(json.dumps(data))

    def set(self, data, overwrite=False):
        assert isinstance(data, dict), 'data must be a dict'

        if overwrite:
            self.write(data)
        else:
            cache = self.read()
            cache.update(data)
            self.write(cache)

    def get(self, key, default=None):
        return self.read().get(key, default)

    def all(self):
        return self.read()
