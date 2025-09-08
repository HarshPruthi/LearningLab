import json
import os
from threading import RLock

class ConfigStore:
    def __init__(self, path: str):
        self.path = path
        self._lock = RLock()
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                f.write(json.dumps({
                    "database": {},
                    "queries": {},
                    "admin": {}
                }, indent=2))

    def load(self):
        with self._lock:
            with open(self.path, "r") as f:
                return json.loads(f.read() or "{}")

    def save(self, data):
        with self._lock:
            with open(self.path, "w") as f:
                f.write(json.dumps(data, indent=2))
