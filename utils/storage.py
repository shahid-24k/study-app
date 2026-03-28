"""
SecureStorage — encrypted local JSON storage.
Uses XOR + base64 obfuscation for lightweight device-local security.
All data stays ON DEVICE. No network calls. No cloud sync.
Security measures:
  - No plain-text sensitive data written to disk
  - No logging of PIN or personal data
  - File stored in app's private directory only
  - No external read/write permissions needed
"""

import json
import os
import base64
import hashlib
from kivy.app import App


_SECRET = b"StudyAppSK2005XR"  # Static obfuscation key (combined with PIN hash in PIN storage)


def _xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def _encode(data: str) -> str:
    raw = data.encode("utf-8")
    obfuscated = _xor_bytes(raw, _SECRET)
    return base64.b64encode(obfuscated).decode("ascii")


def _decode(data: str) -> str:
    try:
        obfuscated = base64.b64decode(data.encode("ascii"))
        raw = _xor_bytes(obfuscated, _SECRET)
        return raw.decode("utf-8")
    except Exception:
        return "{}"


def hash_pin(pin: str) -> str:
    """SHA-256 hash of PIN — never store raw PIN."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


class SecureStorage:
    def __init__(self):
        self._data = {}
        self._path = self._get_path()
        self._load()

    def _get_path(self) -> str:
        try:
            app = App.get_running_app()
            base = app.user_data_dir
        except Exception:
            base = os.path.expanduser("~/.studyapp")
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, ".sd")  # Hidden file, no .json extension

    def _load(self):
        try:
            if os.path.exists(self._path):
                with open(self._path, "r", encoding="ascii") as f:
                    raw = f.read().strip()
                if raw:
                    decoded = _decode(raw)
                    self._data = json.loads(decoded)
        except Exception:
            self._data = {}

    def flush(self):
        try:
            serialized = json.dumps(self._data, separators=(",", ":"))
            encoded = _encode(serialized)
            tmp = self._path + ".tmp"
            with open(tmp, "w", encoding="ascii") as f:
                f.write(encoded)
            os.replace(tmp, self._path)  # Atomic write
        except Exception:
            pass

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self.flush()

    def delete(self, key):
        self._data.pop(key, None)
        self.flush()

    def all_keys(self):
        return list(self._data.keys())
