from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

import PIL.Image

from .utils import LoggedObject

if TYPE_CHECKING:
    import toga


# We need a dummy "internal image format" for the dummy backend It's a wrapper
# around a PIL image. We can't just use a PIL image because that will be
# interpreted *as* a PIL image.
class DummyImage:
    def __init__(self, image=None):
        self.raw = image
        if image:
            buffer = BytesIO()
            self.raw.save(buffer, format="png", compress_level=0)
            self.data = buffer.getvalue()
        else:
            self.data = b"pretend this is PNG image data"


class Image(LoggedObject):
    RAW_TYPE = DummyImage

    def __init__(
        self,
        interface: toga.Image,
        path: Path = None,
        data: bytes = None,
        raw: BytesIO = None,
    ):
        super().__init__()
        self.interface = interface
        if path:
            self._action("load image file", path=path)
            if path.is_file():
                self.native = DummyImage(PIL.Image.open(path))
            else:
                self.native = DummyImage()
        elif data:
            self._action("load image data", data=data)
            self.native = DummyImage(PIL.Image.open(BytesIO(data)))
        else:
            self._action("load image from raw")
            self.native = raw

    def get_width(self):
        if self.native.raw is None:
            return 60
        return self.native.raw.size[0]

    def get_height(self):
        if self.native.raw is None:
            return 40
        return self.native.raw.size[1]

    def get_data(self):
        return self.native.data

    def save(self, path):
        self._action("save", path=path)
