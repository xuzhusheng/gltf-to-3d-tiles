# gltf-to-3d-tiles

glTF to 3d Tiles Converter. Convert glTF model to Glb, b3dm or 3d tiles format.

## Read More
I am writting articles to explain code snippets and methodology used at this repository:
1. [Constructs Bounding Volume Hierarchy(BVH) with Surface Area Heuristic(SAH) in Python](https://xuzhusheng.medium.com/constructs-bounding-volume-hierarchy-bvh-with-surface-area-heuristic-sah-in-python-89c14afb2f03)
2. [3D Affine Transformation Matrices Implementation with NumPy](https://xuzhusheng.medium.com/3d-affine-transformation-matrices-implementation-with-numpy-57f92058403c)
3. [Manipulate JSON with Python Dynamic Object](https://xuzhusheng.medium.com/manipulate-json-with-python-dynamic-object-fe885394d17f)
4. [Converting between Snake Case and Camel Case](https://xuzhusheng.medium.com/converting-between-naming-convention-with-python-2d91032bd0dc)

***

## Usage

```text
λ python main.py  --help
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  b3dm     convert gltf to b3dm
  glb      convert gltf to glb
  tileset  split gltf model to 3d tiles
```

### Glb

```text
λ python main.py glb --help
Usage: main.py glb [OPTIONS] FIN [FOUT]

  convert gltf to glb

Arguments:
  FIN     input gltf path  [required]
  [FOUT]  Optional output glb path (defaults to the path of the input file)

Options:
  --help  Show this message and exit.
```

### b3dm

```text
 λ python main.py b3dm --help
Usage: main.py b3dm [OPTIONS] FIN [FOUT]

  convert gltf to b3dm

Arguments:
  FIN     input gltf path  [required]
  [FOUT]  Optional output b3dm path(defaults to the path of the input file)

Options:
  --help  Show this message and exit.
```

### 3d tiles

```text
 λ python main.py tileset --help
Usage: main.py tileset [OPTIONS] FIN [FOUT]

  split gltf model to 3d tiles

Arguments:
  FIN     input gltf path  [required]
  [FOUT]  Optional output glb path (defaults to the path of the input file)

Options:
  --measure [meter|foot]  measure of attributes in gltf buffers  [default:
                          Measure.METER]
  --up [y|z]              up direction used in gltf coordinate system
                          [default: Axis.Y]
  --help                  Show this message and exit.
```

***
## Support Me
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/jason.xu)
&emsp; [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I5VT4LU)
