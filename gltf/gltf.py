import json
import math
import utils
from .element import Element
from enum import Enum

Z_UP_TO_Y_UP_MATRIX = [1.0, 0.0,  0.0, 0.0, 0.0,
                       0.0, -1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,  0.0, 1.0]


class Axis(str, Enum):
    Y = "y"
    Z = "z"


class Gltf(Element):
    ASSET = {
        "generator": "gltf generator",
        "version": "2.0",
        "copyright": "2019 (p) jason"
    }
    SCENES = [Element(nodes=[0], name="Scene")]
    up_direction = Axis.Y

    def __init__(self, **kwargs) -> None:

        # set default members
        self.asset = Gltf.ASSET
        self.scenes = Gltf.SCENES
        self.scene = 0
        self.nodes = [Element(mesh=0, matrix=Z_UP_TO_Y_UP_MATRIX)
                      ] if Gltf.up_direction is Axis.Y else [Element(mesh=0)]

        super().__init__(False, **kwargs)


class Glb:
    MAGIC = b'glTF'
    VERSION = 2

    CHUNK_JSON = b'JSON'
    CHUNK_BIN = b'BIN'.ljust(4, b'\0')

    def __init__(self, buffers, **kwargs) -> None:
        self.buffers = buffers
        self.__json = Gltf(**kwargs)
        self.__json.buffers = [Element(byte_length=self.buffer_len)]

    @property
    def buffer_len(self):
        bufferLen = 0
        for buffer in self.buffers:
            bufferLen += utils.padded_len(len(buffer))
        return bufferLen

    def get_buffer(self) -> bytearray:
        ret = bytearray()
        for buffer in self.buffers:
            ret += buffer.ljust(utils.padded_len(len(buffer)), b"\0")
        return ret

    def as_bytes(self) -> bytearray:
        ret = bytearray()
        ret += Glb.MAGIC
        ret += utils.int_to_bytes(Glb.VERSION)

        json_chunk = json.dumps(
            self.__json.as_dict(True), separators=(",", ":")).encode()
        json_len = math.ceil(len(json_chunk) / 4) * 4
        json_chunk = json_chunk.ljust(json_len, b" ")
        buffer = self.get_buffer()
        glb_len = 12 + 8 + json_len + 8 + len(buffer)
        ret += utils.int_to_bytes(glb_len)
        ret += utils.int_to_bytes(json_len)
        ret += Glb.CHUNK_JSON
        ret += json_chunk
        ret += utils.int_to_bytes(len(buffer))
        ret += Glb.CHUNK_BIN
        ret += buffer
        return ret
