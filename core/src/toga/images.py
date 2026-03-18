from __future__ import annotations

import importlib
import os
import warnings
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, TypeVar
from warnings import warn

import toga
from toga.platform import entry_points, get_factory

# Make sure deprecation warnings are shown by default
warnings.filterwarnings("default", category=DeprecationWarning)

if TYPE_CHECKING:
    from typing import TypeAlias

    ImageT = TypeVar("ImageT")
    """
    Toga is able to receive and return content in a wide range of image formats.
    ``ImageT`` describes any "image-like" object. This could be an instance of
    [toga.Image][], an image type from a third party library (such as
    [`PIL.Image.Image`][] from Pillow), or the platform's native type for representing
    images.
    """

    # Define the types that can be used as Image content
    PathLikeT: TypeAlias = str | os.PathLike
    BytesLikeT: TypeAlias = bytes | bytearray | memoryview
    ImageLikeT: TypeAlias = Any
    ImageContentT: TypeAlias = PathLikeT | BytesLikeT | ImageLikeT
    """
    When specifying content for an [`toga.Image`][],
    you can provide:

    - a string specifying an absolute or relative path to a file in a
      [known image format][known-image-formats];
    - an absolute or relative [`pathlib.Path`][] object describing a file in a
      [known image format][known-image-formats];
    - a "blob of bytes" data type ([`bytes`][],
      [`bytearray`][], or
      [`memoryview`][]) containing raw image
      data in a
      [known image format][known-image-formats];
    - an instance of [toga.Image][];
    - if [Pillow](https://pillow.readthedocs.io/) is installed, an
      instance of [`PIL.Image.Image`][];
    - an image of a class registered via an
      [image format plugin][image-format-plugins]
      (or a subclass of such a class); or
    - an instance of the
      [native platform image representation][native-image-rep].

    If a relative path is provided, it will be anchored relative to the
    module that defines your Toga application class.
    """

    ExternalImageT = TypeVar("ExternalImageT")
    """
    A type describing an image-like object provided by a third-party library,
    such as [`PIL.Image.Image`][] from Pillow.
    """


class ImageLoadError(Exception):
    """Raised when an image cannot be successfully loaded."""


class ImageConverter(Protocol):
    """A class to convert between an externally defined image type and
    [`toga.Image`][].
    """

    image_class: type[ExternalImageT]
    """The base image class this plugin can interpret."""

    @staticmethod
    def convert_from_format(image_in_format: ExternalImageT) -> BytesLikeT:
        """Convert from [`image_class`][toga.images.ImageConverter.image_class] to
        data in a [known image format][known-image-formats].

        Will accept an instance of
        [`image_class`][toga.images.ImageConverter.image_class],
        or subclass of that class.

        :param image_in_format: An instance of
            [`image_class`][toga.images.ImageConverter.image_class] (or a subclass).
        :returns: The image data, in a [known image format][known-image-formats].
        """

    @staticmethod
    def convert_to_format(
        data: BytesLikeT,
        image_class: type[ExternalImageT],
    ) -> ExternalImageT:
        """Convert from data to [`image_class`][toga.images.ImageConverter.image_class]
        or specified subclass.

        Accepts a bytes-like object representing the image in a
        [known image format][known-image-formats], and returns an instance of the
        image class specified. This image class is guaranteed to be either the
        [`image_class`][toga.images.ImageConverter.image_class] registered by the
        plugin, or a subclass of that class.

        :param data: Image data in a [known image format][known-image-formats].
        :param image_class: The class of image to return.
        :returns: The image, as an instance of the image class specified.
        """


NOT_PROVIDED = object()


class Image:
    def __init__(
        self,
        src: ImageContentT = NOT_PROVIDED,
        *,
        path: object = NOT_PROVIDED,  # DEPRECATED
        data: object = NOT_PROVIDED,  # DEPRECATED
    ):
        """Create a new image.

        :param src: The source from which to load the image. Can be any valid
            [`ImageContentT`][toga.images.ImageContentT] type.
        :param path: **DEPRECATED** - Use `src`.
        :param data: **DEPRECATED** - Use `src`.
        :raises FileNotFoundError: If a path is provided, but that path does not exist.
        :raises ValueError: If the source cannot be loaded as an image.
        """
        ######################################################################
        # 2023-11: Backwards compatibility for <= 0.4.0
        ######################################################################
        num_provided = sum(arg is not NOT_PROVIDED for arg in (src, path, data))
        if num_provided > 1:
            raise TypeError("Received multiple arguments to constructor.")
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

        self.factory = get_factory()
        self._path = None

        # Any "lump of bytes" should be valid here.
        if isinstance(src, bytes | bytearray | memoryview):
            try:
                self._impl = self.factory.Image(interface=self, data=src)
            except ImageLoadError as exc:
                raise ValueError("Unable to load image from data") from exc

        elif isinstance(src, str | Path):
            self._path = toga.App.app.paths.app / src
            if not self._path.is_file():
                raise FileNotFoundError(f"Image file {self._path} does not exist")
            data = self._path.read_bytes()
            try:
                self._impl = self.factory.Image(interface=self, data=data)
            except ImageLoadError as exc:
                raise ValueError(f"Unable to load image from {self._path}") from exc

        elif isinstance(src, Image):
            self._impl = self.factory.Image(interface=self, data=src.data)

        elif isinstance(src, self.factory.Image.RAW_TYPE):
            self._impl = self.factory.Image(interface=self, raw=src)

        else:
            for converter in self._converters():
                if isinstance(src, converter.image_class):
                    data = converter.convert_from_format(src)
                    self._impl = self.factory.Image(interface=self, data=data)
                    return

            raise TypeError("Unsupported source type for Image")

    @classmethod
    @cache
    def _converters(cls) -> list[ImageConverter]:
        """Return list of registered image plugin converters. Only loaded once."""
        converters = []

        for image_plugin in entry_points(group="toga.image_formats"):
            module_name, class_name = image_plugin.value.rsplit(".", 1)
            module = importlib.import_module(module_name)
            converter = getattr(module, class_name)

            if converter.image_class is not None:
                converters.append(converter)

        return converters

    @property
    def size(self) -> tuple[int, int]:
        """The size of the image, as a (width, height) tuple."""
        return self._impl.get_width(), self._impl.get_height()

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
        the filename provided (e.g `path/to/mypicture.png` will save a PNG file).

        :param path: Path to save the image to.
        """
        self._impl.save(path)

    def as_format(self, format: type[ImageT]) -> ImageT:
        """Return the image, converted to the image format specified.

        :param format: Format to provide. Defaults to [`Image`][toga.images.Image]; also
             supports [`PIL.Image.Image`][] if Pillow is installed, as well as any
             image types defined by installed
             [image format plugin][image-format-plugins].
        :returns: The image in the requested format
        :raises TypeError: If the format supplied is not recognized.
        """
        if isinstance(format, type):
            if issubclass(format, Image):
                return format(self.data)

            for converter in self._converters():
                if issubclass(format, converter.image_class):
                    return converter.convert_to_format(self.data, format)

        raise TypeError(f"Unknown conversion format for Image: {format}")
