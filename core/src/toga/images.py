from __future__ import annotations

from pathlib import Path

import toga
from toga.platform import get_platform_factory


class Image:
    def __init__(
        self,
        path: str | None | Path = None,
        *,
        data: bytes | None = None,
    ):
        """Create a new image.

        An image must be provided either a ``path`` or ``data``, but not both.

        :param path: Path to the image to load. This can be specified as a string, or as
            a :any:`pathlib.Path` object. The path can be an absolute file system path,
            or a path relative to the module that defines your Toga application class.
        :param data: A bytes object with the contents of an image in a supported format.
        :raises FileNotFoundError: If a path is provided, but that path does not exist.
        :raises ValueError: If the path or data cannot be loaded as an image.
        """
        if path is None and data is None:
            raise ValueError("Either path or data must be set.")
        if path is not None and data is not None:
            raise ValueError("Only either path or data can be set.")

        if path is not None:
            if isinstance(path, Path):
                self.path = path
            else:
                self.path = Path(path)
        else:
            self.path = None

        self.factory = get_platform_factory()
        if data is not None:
            self._impl = self.factory.Image(interface=self, data=data)
        else:
            self.path = toga.App.app.paths.app / self.path
            if not self.path.is_file():
                raise FileNotFoundError(f"Image file {self.path} does not exist")
            self._impl = self.factory.Image(interface=self, path=self.path)

    @property
    def size(self) -> (int, int):
        """The size of the image, as a tuple"""
        return (self._impl.get_width(), self._impl.get_height())

    @property
    def width(self) -> int:
        """The width of the image, in pixels."""
        return self._impl.get_width()

    @property
    def height(self) -> int:
        """The height of the image, in pixels."""
        return self._impl.get_height()

    @property
    def data(self) -> bytes:
        """The raw data for the image, in PNG format.

        :returns: The raw image data in PNG format.
        """
        return self._impl.get_data()

    def save(self, path: str | Path):
        """Save image to given path.

        The file format of the saved image will be determined by the extension of
        the filename provided (e.g ``path/to/mypicture.png`` will save a PNG file).

        :param path: Path where to save the image.
        """
        self._impl.save(path)
