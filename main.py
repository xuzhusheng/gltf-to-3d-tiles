import typer
from gltf_to_tileset import gltf_to_tileset
from tileset import Measure
from gltf import Glb, Element
import json
from pathlib import Path
from tileset import B3dm
import shutil
import timeit
from urllib.request import urlopen

app = typer.Typer()


def is_data_uri(uri):
    return uri.startswith("data:")


def read_buffer(uri, parent):
    if is_data_uri(uri):
        with urlopen(uri) as response:
            return response.read()

    with open(parent / uri, "rb") as f:
        return f.read()


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


def copy_textures(fin, fout, images):
    src_parent = Path(fin).parent
    dest_parent = Path(fout).parent
    if src_parent == dest_parent:
        return

    for image in images:
        dest = dest_parent / image.uri
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_parent / image.uri, dest)


@app.command()
def tileset(fin: str = typer.Argument(..., help="input gltf path"), fout: str = typer.Argument(None, help="Optional output glb path (defaults to the path of the input file)"), measure: Measure = typer.Option(Measure.METER, help="measure of attributes in gltf buffers")):
    """split gltf model to 3d tiles"""
    start = timeit.default_timer()
    gltf, buffer = read_gltf(fin)

    if not fout:
        fout = Path(fin).parent / "tileset.json"

    gltf_to_tileset(gltf, buffer, fout, measure)
    copy_textures(fin, fout, gltf.images)
    end = timeit.default_timer()
    typer.echo(f"completed in: {end - start}s")


@app.command()
def glb(fin: str = typer.Argument(..., help="input gltf path"), fout: str = typer.Argument(None, help="Optional output glb path (defaults to the path of the input file)")):
    """convert gltf to glb"""
    gltf, buffer = read_gltf(fin)

    if not fout:
        fout = Path(fin).with_suffix(".glb")
    with open(fout, "wb") as f:
        f.write(Glb(buffer, **gltf.as_dict(False)).as_bytes())
    copy_textures(fin, fout, gltf.images)
    typer.echo("completed")


@app.command()
def b3dm(fin: str = typer.Argument(..., help="input gltf path"), fout: str = typer.Argument(None, help="Optional output b3dm path(defaults to the path of the input file)")):
    """convert gltf to b3dm"""
    gltf, buffer = read_gltf(fin)

    if not fout:
        fout = Path(fin).with_suffix(".b3dm")

    with open(fout, "wb") as f:
        f.write(B3dm("b3dm", Glb(buffer, **gltf.as_dict(False)).as_bytes()).as_bytes())
    copy_textures(fin, fout, gltf.images)
    typer.echo("completed")


if __name__ == "__main__":
    app()
