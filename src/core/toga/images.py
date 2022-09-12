import pathlib


class Image:
    """
    A representation of graphical content.

    :param path: Path to the image. Allowed values can be local file
        (relative or absolute path) or URL (HTTP or HTTPS). Relative paths
        will be interpreted relative to the application module directory.
    TODO: or bytes object containig a valid image...
    """
    def __init__(self, value=None, path=None):
        if path is not None:
            value = path  #TODO: code to deprecate path
        self.data = None
        self.path = None

        if isinstance(value, bytes):
            self.data = value
        elif isinstance(value, pathlib.Path):
            self.path = value
        elif value.startswith('http://') or value.startswith('https://'):
            self.path = value
        else:
            self.path = pathlib.Path(value)

        # Resource is late bound.
        self._impl = None

    def bind(self, factory):
        """
        Bind the Image to a factory.

        Creates the underlying platform implementation of the Image. Raises
        FileNotFoundError if the path is a non-existent local file.

        :param factory: The platform factory to bind to.
        :returns: The platform implementation
        """
        if self._impl is None:
            if self.data is not None:
                self._impl = factory.Image(interface=self, data=self.data)
            elif isinstance(self.path, pathlib.Path):
                full_path = factory.paths.app / self.path
                if not full_path.exists():
                    raise FileNotFoundError(
                        'Image file {full_path!r} does not exist'.format(
                            full_path=full_path
                        )
                    )
                self._impl = factory.Image(interface=self, path=full_path)
            else:
                self._impl = factory.Image(interface=self, url=self.path)

        return self._impl
