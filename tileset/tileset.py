
class Tileset:
    ASSET = {"version": "1.0",
             "tilesetVersion": "1.0.0.0"}

    def __init__(self, root) -> None:
        self.root = root

    @ property
    def geometric_error(self):
        return self.root.geometric_error

    @ property
    def dict(self):
        return {
            "asset": Tileset.ASSET,
            "geometricError": self.geometric_error,
            "root": self.root.dict
        }
