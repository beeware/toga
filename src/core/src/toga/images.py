import pathlib
import warnings

from toga.platform import get_platform_factory


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

        if path:
            if isinstance(path, pathlib.Path):
                self.path = path
            elif path.startswith("http://") or path.startswith("https://"):
                self.path = path
            else:
                self.path = pathlib.Path(path)
        else:
            self.path = None
        self.data = data

        # Resource is late bound.
        self._impl = None

    def bind(
        self,
        factory=None,  # DEPRECATED !
    ):
        """Bind the Image to a factory.

        Creates the underlying platform implementation of the Image. Raises
        FileNotFoundError if the path is a non-existent local file.

        :returns: The platform implementation
        """
        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        factory = get_platform_factory()
        if self._impl is None:
            if self.data is not None:
                self._impl = factory.Image(interface=self, data=self.data)
            elif isinstance(self.path, pathlib.Path):
                full_path = factory.paths.app / self.path
                if not full_path.exists():
                    raise FileNotFoundError(
                        "Image file {full_path!r} does not exist".format(
                            full_path=full_path
                        )
                    )
                self._impl = factory.Image(interface=self, path=full_path)
            else:
                self._impl = factory.Image(interface=self, url=self.path)

        return self._impl
