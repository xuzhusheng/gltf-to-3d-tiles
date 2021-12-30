import json
import utils
import struct
from .content import Content


class I3dm(Content):
    __MAGIC = b'i3dm'
    GLTF_FORMAT = 1
    __HEADER_LEN = 32

    def __init__(self, name: str, content: bytes, matrices: list, *, extras=None) -> None:
        super().__init__(name, content, extras=extras)
        self.__matrices = matrices

    def _magic(self):
        return I3dm.__MAGIC

    def _header_len(self):
        return I3dm.__HEADER_LEN

    @ property
    def uri(self):
        return self._name + ".i3dm"

    def feature_json(self):
        instances_count = len(self.__matrices)
        return json.dumps({
            "INSTANCES_LENGTH": instances_count,
            "POSITION": {
                "byteOffset": 0
            },
            "NORMAL_UP": {
                "byteOffset": instances_count * 12
            },
            "NORMAL_RIGHT": {
                "byteOffset": instances_count * 24
            },
            "SCALE_NON_UNIFORM": {
                "byteOffset": instances_count * 36
            }
        }, separators=(",", ":")).encode("utf-8")

    def _feature_bin(self):
        positions = []
        ups = []
        rights = []
        scales = []
        for matrix in self.__matrices:
            positions += matrix.position
            ups += matrix.up
            rights += matrix.right
            scales += matrix.scale
        ret = positions + ups + rights + scales
        return struct.pack('<%sf' % len(ret), *ret)

    def as_bytes(self) -> bytes:
        return self._header() + utils.int_to_bytes(1) + self._body()
