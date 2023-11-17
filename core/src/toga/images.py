from __future__ import annotations

import warnings
from io import BytesIO
from pathlib import Path
from typing import Any
from warnings import warn

try:
    import PIL.Image as PIL_Image
except ImportError:  # pragma: no cover
    PIL_Image = None

import toga
from toga.platform import get_platform_factory

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)


class Image:
    def __init__(
        self,
        src: str | Path | bytes | PIL_Image.Image | None = None,
        *,
        path=None,  # DEPRECATED
        data=None,  # DEPRECATED
    ):
        """Create a new image.

        :param src: The source from which to load the image. Can be a filepath
            (relative or absolute, as a string or :any:`pathlib.Path`), raw binary data
            in any supported image format, or a `Pillow <https://python-pillow.org/>`_
            ``Image``.
        :param path: **DEPRECATED** - Use ``src``.
        :param data: **DEPRECATED** - Use ``src``.
        :raises FileNotFoundError: If a path is provided, but that path does not exist.
        :raises ValueError: If the source cannot be loaded as an image.
        """
        ######################################################################
        # 2023-11: Backwards compatibility
        ######################################################################
        num_provided = sum(arg is not None for arg in (src, path, data))
        if num_provided > 1:
            raise ValueError("Received multiple arguments to constructor.")
        if num_provided == 0:
            raise ValueError("No image source supplied.")
        if path is not None:
            src = path
            warn(
                "Path argument is deprecated, use src instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        elif data is not None:
            src = data
            warn(
                "Data argument is deprecated, use src instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        ######################################################################
        # End backwards compatibility
        ######################################################################

        self.factory = get_platform_factory()
        self._path = None

        if isinstance(src, bytes):
            self._impl = self.factory.Image(interface=self, data=src)

        elif isinstance(src, (str, Path)):
            self._path = toga.App.app.paths.app / src
            if not self._path.is_file():
                raise FileNotFoundError(f"Image file {self._path} does not exist")
            self._impl = self.factory.Image(interface=self, path=self._path)

        elif isinstance(src, PIL_Image.Image):
            buffer = BytesIO()
            src.save(buffer, format="png", compress_level=0)
            self._impl = self.factory.Image(interface=self, data=buffer.getvalue())

        else:
            raise TypeError("Unsupported source type for Image")

    @property
    def size(self) -> (int, int):
        """The size of the image, as a tuple."""
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
        """The raw data for the image, in PNG format."""
        return self._impl.get_data()

    @property
    def path(self) -> Path | None:
        """The path from which the image was opened, if any (or None)."""
        return self._path

    def save(self, path: str | Path) -> None:
        """Save image to given path.

        The file format of the saved image will be determined by the extension of
        the filename provided (e.g ``path/to/mypicture.png`` will save a PNG file).

        :param path: Path where to save the image.
        """
        self._impl.save(path)

    def as_format(self, format: type) -> Any:
        """Return the image, converted to the image format specified.

        :param format: The image class to return. Currently supports only :class:`Image`
            (which simply returns self) and ``Image`` from from
            `Pillow <https://python-pillow.org/>`_.
        :returns: The image in the requested format
        :raises TypeError: If the format supplied is not recognized.
        """
        if format is Image:
            # This is mostly here to simplify calling logic.
            return self

        if PIL_Image is not None and format is PIL_Image.Image:
            buffer = BytesIO(self.data)
            return PIL_Image.open(buffer)

        raise TypeError(f"Unknown conversion format for Image: {format}")
