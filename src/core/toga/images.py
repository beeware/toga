class Image:
    """
    A representation of graphical content.

    :param path: Path to the image. Allowed values can be local file
        (relative or absolute path) or URL (HTTP or HTTPS). Relative paths
        will be interpreted relative to the application module directory.
    """
    def __init__(self, path):
        self.path = path

        # Resource is late bound.
        self._impl = None

    def bind(self, factory):
        """
        Bind the Image to a factory.

        Creates the underlying platform implemenation of the Image. Raises
        FileNotFoundError if the path is a non-existent local file.

        :param factory: The platform factory to bind to.
        :returns: The platform implementation
        """
        if self._impl is None:
            if self.path.startswith('http://') or self.path.startswith('https://'):
                self._impl = factory.Image(interface=self, url=self.path)
            else:
                full_path = factory.paths.app / factory.paths.Path(self.path)
                if not full_path.exists():
                    raise FileNotFoundError(
                        'Image file {full_path!r} does not exist'.format(
                            full_path=full_path
                        )
                    )
                self._impl = factory.Image(interface=self, path=full_path)

        return self._impl
