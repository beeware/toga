from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

import PIL.Image

from .utils import LoggedObject

if TYPE_CHECKING:
    import toga


class Image(LoggedObject):
    def __init__(self, interface: toga.Image, path: Path = None, data: bytes = None):
        super().__init__()
        self.interface = interface
        if path:
            self._action("load image file", path=path)
            if path.is_file():
                self._data = path.read_bytes()
                with PIL.Image.open(path) as image:
                    self._width, self._height = image.size
            else:
                self._data = b"pretend this is PNG image data"
                self._width, self._height = 60, 40
        else:
            self._action("load image data", data=data)
            self._data = data
            buffer = BytesIO(data)
            with PIL.Image.open(buffer) as image:
                self._width, self._height = image.size

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_data(self):
        return self._data

    def save(self, path):
        self._action("save", path=path)
