import utils
from abc import ABC, abstractmethod


class Content(ABC):
    VERSION = 1

    def __init__(self, name: str, content: bytes) -> None:
        self._name = name
        # self._box = box
        self.content = content

    @abstractmethod
    def _magic(self):
        pass

    @ property
    @abstractmethod
    def uri(self):
        pass

    @ property
    def dict(self):
        return {
            "uri": self.uri
            # "boundingVolume": {"box": self._box.list}
        }

    @abstractmethod
    def feature_json(self):
        pass

    def _feature_json_len(self):
        return utils.padded_len(len(self.feature_json()) + self._header_len(), padding=8) - self._header_len()

    @abstractmethod
    def _header_len(self):
        pass

    def _header(self) -> bytes:
        ret = bytearray(self._magic())
        ret += utils.int_to_bytes(Content.VERSION)
        # feature_json = self.feature_json()
        feature_json_len = self._feature_json_len()
        feature_bytes = self._feature_bin()
        feature_bytes_len = len(feature_bytes)
        ret += utils.int_to_bytes(self._header_len() +
                                  feature_json_len + feature_bytes_len + len(self.content))
        ret += utils.int_to_bytes(feature_json_len)
        ret += utils.int_to_bytes(feature_bytes_len)
        ret += utils.int_to_bytes(0) * 2
        return ret

    def _feature_bin(self):
        return b''

    def _body(self) -> bytes:
        feature_json = self.feature_json()
        # feature_json_len = utils.padded_len(len(feature_json))
        ret = bytearray(feature_json.ljust(self._feature_json_len(), b' '))
        feature_bytes = self._feature_bin()
        ret += feature_bytes
        ret += self.content
        return ret

    @abstractmethod
    def as_bytes(self) -> bytes:
        pass
