import utils
from abc import ABC, abstractmethod
import json


class Content(ABC):
    VERSION = 1

    def __init__(self, name: str, content: bytes, *, extras=None) -> None:
        self._name = name
        # self._box = box
        self.content = content
        self.__extras = extras

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

    def _batch_json(self):
        if self.__extras:
            return json.dumps({"extras": self.__extras}, separators=(",", ":")).encode("utf-8")
        return b''

    def _batch_json_len(self):
        return utils.padded_len((len(self._batch_json())), padding=8)

    def _feature_json_len(self):
        return utils.padded_len(len(self.feature_json()) + self._header_len(), padding=8) - self._header_len()

    @abstractmethod
    def _header_len(self):
        pass

    def _byte_len(self):
        return self._header_len() + self._feature_json_len() + len(self._feature_bin()) + self._batch_json_len() + len(self.content)

    def _header(self) -> bytes:
        ret = bytearray(self._magic())
        ret += utils.int_to_bytes(Content.VERSION)
        # feature_json = self.feature_json()
        feature_json_len = self._feature_json_len()
        feature_bytes = self._feature_bin()
        feature_bytes_len = len(feature_bytes)
        batch_json_len = self._batch_json_len()
        ret += utils.int_to_bytes(utils.padded_len(self._byte_len()))
        ret += utils.int_to_bytes(feature_json_len)
        ret += utils.int_to_bytes(feature_bytes_len)
        ret += utils.int_to_bytes(batch_json_len)
        ret += utils.int_to_bytes(0)
        return ret

    def _feature_bin(self):
        return b''

    def _body(self) -> bytes:
        feature_json = self.feature_json()
        # feature_json_len = utils.padded_len(len(feature_json))
        ret = bytearray(feature_json.ljust(self._feature_json_len(), b' '))
        feature_bytes = self._feature_bin()
        ret += feature_bytes
        ret += bytearray(self._batch_json().ljust(self._batch_json_len(), b' '))
        ret += self.content
        byteLen = self._byte_len()
        padding = utils.padded_len(byteLen) - byteLen
        ret += b'\0' * padding
        return ret

    @abstractmethod
    def as_bytes(self) -> bytes:
        pass
