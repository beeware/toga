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

        :param path: Path to the image. This can be an absolute path to an image
            file, or a path relative to the file that describes the App class.
            Can be specified as a string, or as a :any:`pathlib.Path` object.
        :param data: A bytes object with the contents of an image in a supported
            format.
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
            self.data = None
        else:
            self.path = None
            self.data = data

        self.factory = get_platform_factory()
        if self.data is not None:
            self._impl = self.factory.Image(interface=self, data=self.data)
        else:
            self.path = toga.App.app.paths.app / self.path
            if not self.path.is_file():
                raise FileNotFoundError(f"Image file {self.path} does not exist")
            self._impl = self.factory.Image(interface=self, path=self.path)

    @property
    def width(self) -> int:
        """The width of the image, in pixels."""
        return self._impl.get_width()

    @property
    def height(self) -> int:
        """The height of the image, in pixels."""
        return self._impl.get_height()

    def save(self, path):
        """Save image to given path.

        :param path: Path where to save the image.
        """
        self._impl.save(path)
