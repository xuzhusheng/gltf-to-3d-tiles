import json
import math
import utils
from .element import Element

Z_UP_TO_Y_UP_MATRIX = [1.0, 0.0,  0.0, 0.0, 0.0,
                       0.0, -1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,  0.0, 1.0]


class Gltf(Element):
    ASSET = {
        "generator": "gltf generator",
        "version": "2.0",
        "copyright": "2019 (p) jason"
    }
    SCENES = [Element(nodes=[0], name="Scene")]
    NODES = [Element(mesh=0, matrix=Z_UP_TO_Y_UP_MATRIX)]

    def __init__(self, **kwargs) -> None:

        # set default members
        self.asset = Gltf.ASSET
        self.scenes = Gltf.SCENES
        self.scene = 0
        self.nodes = Gltf.NODES

        super().__init__(False, **kwargs)


class Glb:
    MAGIC = b'glTF'
    VERSION = 2

    CHUNK_JSON = b'JSON'
    CHUNK_BIN = b'BIN'.ljust(4, b'\0')

    def __init__(self, buffer, **kwargs) -> None:
        self.buffer = buffer
        self.__json = Gltf(**kwargs)
        self.__json.buffers = [Element(byte_length=self.buffer_len)]

    @property
    def buffer_len(self):
        return utils.padded_len(len(self.buffer))

    def as_bytes(self) -> bytearray:
        ret = bytearray()
        ret += Glb.MAGIC
        ret += utils.int_to_bytes(Glb.VERSION)

        json_chunk = json.dumps(
            self.__json.as_dict(True), separators=(",", ":")).encode()
        json_len = math.ceil(len(json_chunk) / 4) * 4
        json_chunk = json_chunk.ljust(json_len, b" ")
        buffer = self.buffer.ljust(self.buffer_len, b"\0")
        glb_len = 12 + 8 + json_len + 8 + self.buffer_len
        ret += utils.int_to_bytes(glb_len)
        ret += utils.int_to_bytes(json_len)
        ret += Glb.CHUNK_JSON
        ret += json_chunk
        ret += utils.int_to_bytes(self.buffer_len)
        ret += Glb.CHUNK_BIN
        ret += buffer
        return ret
