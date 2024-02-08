from __future__ import annotations

import importlib
import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any
from warnings import warn

import toga
from toga.platform import get_platform_factory

if sys.version_info >= (3, 10):
    from importlib.metadata import entry_points
else:
    # Before Python 3.10, entry_points did not support the group argument;
    # so, the backport package must be used on older versions.
    from importlib_metadata import entry_points

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)

if TYPE_CHECKING:
    if sys.version_info < (3, 10):
        from typing_extensions import TypeAlias, TypeVar
    else:
        from typing import TypeAlias, TypeVar

    # Define a type variable for generics where an Image type is required.
    ImageT = TypeVar("ImageT")

    # Define the types that can be used as Image content
    PathLike: TypeAlias = str | Path
    BytesLike: TypeAlias = bytes | bytearray | memoryview
    ImageLike: TypeAlias = Any
    ImageContent: TypeAlias = PathLike | BytesLike | ImageLike


NOT_PROVIDED = object()


class Image:
    converters = {}

    def __init__(
        self,
        src: ImageContent = NOT_PROVIDED,
        *,
        path=NOT_PROVIDED,  # DEPRECATED
        data=NOT_PROVIDED,  # DEPRECATED
    ):
        """Create a new image.

        :param src: The source from which to load the image. Can be any valid
            :any:`image content <ImageContent>` type.
        :param path: **DEPRECATED** - Use ``src``.
        :param data: **DEPRECATED** - Use ``src``.
        :raises FileNotFoundError: If a path is provided, but that path does not exist.
        :raises ValueError: If the source cannot be loaded as an image.
        """
        ######################################################################
        # 2023-11: Backwards compatibility
        ######################################################################
        num_provided = sum(arg is not NOT_PROVIDED for arg in (src, path, data))
        if num_provided > 1:
            raise ValueError("Received multiple arguments to constructor.")
        if num_provided == 0:
            raise TypeError(
                "Image.__init__() missing 1 required positional argument: 'src'"
            )
        if path is not NOT_PROVIDED:
            src = path
            warn(
                "Path argument is deprecated, use src instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        elif data is not NOT_PROVIDED:
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

        # Any "lump of bytes" should be valid here.
        if isinstance(src, (bytes, bytearray, memoryview)):
            self._impl = self.factory.Image(interface=self, data=src)

        elif isinstance(src, (str, Path)):
            self._path = toga.App.app.paths.app / src
            if not self._path.is_file():
                raise FileNotFoundError(f"Image file {self._path} does not exist")
            self._impl = self.factory.Image(interface=self, path=self._path)

        elif isinstance(src, Image):
            self._impl = self.factory.Image(interface=self, data=src.data)

        elif isinstance(src, self.factory.Image.RAW_TYPE):
            self._impl = self.factory.Image(interface=self, raw=src)

        else:
            # If it's a registered format, convert as necessary.
            if converter := self.converters.get(src.__class__):
                data = converter.convert_from_format(src)
                self._impl = self.factory.Image(interface=self, data=data)
                return

            # If it's a subclass of a registered format, convert and also save it so it
            # doesn't have to be searched for next time.
            for image_class, converter in self.converters.items():
                if isinstance(src, image_class):
                    self.converters[src.__class__] = converter
                    data = converter.convert_from_format(src)
                    self._impl = self.factory.Image(interface=self, data=data)
                    return

            raise TypeError("Unsupported source type for Image")

    @classmethod
    def load_converters(cls):
        for image_format in entry_points(group="toga.image_formats"):
            converter = importlib.import_module(f"{image_format.value}.converter")
            cls.converters[converter.image_class] = converter

    @property
    def size(self) -> (int, int):
        """The size of the image, as a (width, height) tuple."""
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

        :param path: Path to save the image to.
        """
        self._impl.save(path)

    def as_format(self, format: type[ImageT]) -> ImageT:
        """Return the image, converted to the image format specified.

        :param format: The image class to return. Currently supports only :any:`Image`,
            and :any:`PIL.Image.Image` if Pillow is installed.
        :returns: The image in the requested format
        :raises TypeError: If the format supplied is not recognized.
        """
        if isinstance(format, type):
            if issubclass(format, Image):
                return format(self.data)

            # If it's a registered format, convert as necessary.
            if converter := self.converters.get(format):
                return converter.convert_to_format(self.data, format)

            # If it's a subclass of a registered format, convert and also save it so it
            # doesn't have to be searched for next time.
            for image_class, converter in self.converters.items():
                if issubclass(format, image_class):
                    self.converters[format] = converter
                    return converter.convert_to_format(self.data, format)

        raise TypeError(f"Unknown conversion format for Image: {format}")
