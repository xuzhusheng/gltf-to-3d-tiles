import json
from .content import Content

class B3dm(Content):
    __MAGIC = b'b3dm'
    __FEATURE_JSON = json.dumps(
        {"BATCH_LENGTH": 0}, separators=(",", ":")).encode("utf-8")
    __HEADER_LEN = 28

    def _magic(self):
        return B3dm.__MAGIC

    def _header_len(self):
        return B3dm.__HEADER_LEN

    @ property
    def uri(self):
        return self._name + ".b3dm"

    def feature_json(self):
        return B3dm.__FEATURE_JSON

    def as_bytes(self) -> bytes:
        return self._header() + self._body()
