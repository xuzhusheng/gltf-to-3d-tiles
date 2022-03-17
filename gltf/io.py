from pathlib import Path
from urllib.request import urlopen
from .element import Element
import json
import shutil
import logging


logger = logging.getLogger(__name__)


def read_gltf(fin):
    with open(fin, encoding='utf-8') as f:
        gltf = json.load(f, object_hook=lambda d: Element(**d))

    # buffers = []
    # for buffer in gltf.buffers:
    #     buffers.append(read_buffer(buffer.uri))
    # with open(Path(fin).parent / gltf.buffers[0].uri, "rb") as f:
    #     buffer = f.read()
    buffer = read_buffer(gltf.buffers[0].uri, Path(fin).parent)

    return gltf, buffer


def read_buffer(uri, parent):
    if is_data_uri(uri):
        with urlopen(uri) as response:
            return response.read()

    with open(parent / uri, "rb") as f:
        return f.read()


def is_data_uri(uri):
    return uri.startswith("data:")


def copy_textures(fin, fout, images):
    if not images:
        return

    src_parent = Path(fin).parent
    dest_parent = Path(fout).parent
    if src_parent == dest_parent:
        return

    for image in images:
        dest = dest_parent / image.uri
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src_parent / image.uri, dest)
        except Exception as e:
            logger.error(e)
