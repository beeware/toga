from __future__ import annotations

import sys
import warnings
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any
from warnings import warn

try:
    import PIL.Image

    PIL_imported = True
except ImportError:  # pragma: no cover
    PIL_imported = False

import toga
from toga.platform import get_platform_factory

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

        elif PIL_imported and isinstance(src, PIL.Image.Image):
            buffer = BytesIO()
            src.save(buffer, format="png", compress_level=0)
            self._impl = self.factory.Image(interface=self, data=buffer.getvalue())

        elif isinstance(src, self.factory.Image.RAW_TYPE):
            self._impl = self.factory.Image(interface=self, raw=src)

        else:
            raise TypeError("Unsupported source type for Image")

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
        if isinstance(format, type) and issubclass(format, Image):
            return format(self.data)

        if PIL_imported and format is PIL.Image.Image:
            buffer = BytesIO(self.data)
            with PIL.Image.open(buffer) as pil_image:
                pil_image.load()
            return pil_image

        raise TypeError(f"Unknown conversion format for Image: {format}")
