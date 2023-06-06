import re
from pathlib import Path

import toga
from toga.platform import get_platform_factory

URL_RE = re.compile(r"\w+://")


class Image:
    """A representation of graphical content.

    :param path: Path to the image. Allowed values can be local file
        (relative or absolute path) or URL (HTTP or HTTPS). Relative paths
        will be interpreted relative to the application module directory.
    :param data: A bytes object with the contents of an image in a supported
        format.
    """

    def __init__(self, path=None, *, data=None):
        if path is None and data is None:
            raise ValueError("Either path or data must be set.")
        if path is not None and data is not None:
            raise ValueError("Only either path or data can be set.")

        if path is not None:
            if isinstance(path, Path):
                self.path = path
            elif path.startswith("http://") or path.startswith("https://"):
                self.path = path
            elif path.startswith("file://"):
                self.path = Path(path[7:])
            elif URL_RE.match(path):
                raise ValueError(
                    "Images can only be loaded from http://, https:// or file:// URLs"
                )
            else:
                self.path = Path(path)
        else:
            self.path = None
        self.data = data

        self.factory = get_platform_factory()
        if self.data is not None:
            self._impl = self.factory.Image(interface=self, data=self.data)
        elif isinstance(self.path, Path):
            self.path = toga.App.app.paths.app / self.path
            if not self.path.is_file():
                raise FileNotFoundError(f"Image file {self.path} does not exist")
            self._impl = self.factory.Image(interface=self, path=self.path)
        else:
            self._impl = self.factory.Image(interface=self, url=self.path)

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
