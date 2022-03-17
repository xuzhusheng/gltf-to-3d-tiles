import typer
from converter.gltf_to_tileset import gltf_to_tileset
from tileset import Measure
from gltf import Glb, Element, io
import json
from pathlib import Path
from tileset import B3dm
import timeit
from urllib.request import urlopen
import logging

app = typer.Typer()
logger = logging.getLogger(__name__)


@app.command()
def tileset(
        fin: str = typer.Argument(..., help="input gltf path"),
        fout: str = typer.
    Argument(
        None,
        help="Optional output glb path (defaults to the path of the input file)"
            ),
        measure: Measure = typer.Option(
            Measure.METER, help="measure of attributes in gltf buffers")):
    """split gltf model to 3d tiles"""
    start = timeit.default_timer()

    if not fout:
        fout = Path(fin).parent / "tileset.json"

    gltf_to_tileset(fin, fout, measure)
    end = timeit.default_timer()
    typer.echo(f"completed in: {end - start}s")


@app.command()
def glb(
        fin: str = typer.Argument(..., help="input gltf path"),
        fout: str = typer.
    Argument(
        None,
        help="Optional output glb path (defaults to the path of the input file)"
            )):
    """convert gltf to glb"""
    gltf, buffer = io.read_gltf(fin)

    if not fout:
        fout = Path(fin).with_suffix(".glb")
    with open(fout, "wb") as f:
        f.write(Glb(buffer, **gltf.as_dict(False)).as_bytes())
    io.copy_textures(fin, fout, gltf.images)
    typer.echo("completed")


@app.command()
def b3dm(
        fin: str = typer.Argument(..., help="input gltf path"),
        fout: str = typer.
    Argument(
        None,
        help="Optional output b3dm path(defaults to the path of the input file)"
            )):
    """convert gltf to b3dm"""
    gltf, buffer = io.read_gltf(fin)

    if not fout:
        fout = Path(fin).with_suffix(".b3dm")

    with open(fout, "wb") as f:
        f.write(
            B3dm("b3dm",
                 Glb(buffer, **gltf.as_dict(False)).as_bytes()).as_bytes())
    io.copy_textures(fin, fout, gltf.images)
    typer.echo("completed")


if __name__ == "__main__":
    app()
