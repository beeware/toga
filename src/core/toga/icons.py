import os


class Icon:
    """
    Icon widget.

    Icon is a deferred resource - it's impl isn't available until it the icon
    is assigned to perform a role in an app. At the point at which the Icon is
    used, the Icon is bound to a factory, and the implementation is created.

    :param path: The path to the icon file, relative to the application's
        module directory.
    :param system: Is this a system resource? Set to ``True`` if the icon is
        one of the Toga-provided icons. Default is False.
    """

    def __init__(self, path, system=False):
        self.path = path

        self.system = system

        self._impl = None

    @property
    def filename(self):
        if self.system:
            toga_dir = os.path.dirname(__file__)
            return os.path.join(toga_dir, self.path)
        else:
            # no resource dir so default to the file path
            return self.path

    def bind(self, factory):
        if self._impl is None:
            try:
                if factory.Icon.SIZES:
                    file_path = {
                        size: self._icon_file_path(
                            size=size,
                            extensions=factory.Icon.EXTENSIONS,
                            app_path=factory.paths.app,
                        )
                        for size in factory.Icon.SIZES
                    }
                else:
                    file_path = self._icon_file_path(
                        size=None,
                        extensions=factory.Icon.EXTENSIONS,
                        app_path=factory.paths.app,
                    )

                self._impl = factory.Icon(interface=self, file_path=file_path)
            except FileNotFoundError:
                print("WARNING: Can't find icon {self.path}; falling back to default icon".format(
                    self=self
                ))
                self._impl = self.TOGA_ICON.bind(factory)

        return self._impl

    def _icon_file_path(self, size, extensions, app_path):
        basename, file_extension = os.path.splitext(self.filename)

        if not file_extension:
            # If no extension is provided, look for one of the allowed
            # icon types, in preferred format order.
            for extension in extensions:
                # look for an icon file with a size in the filename
                icon_path = app_path / (
                    '{basename}-{size}{extension}'.format(
                        basename=basename,
                        size=size,
                        extension=extension
                    )
                )
                if icon_path.exists():
                    return icon_path

                # look for a icon file without a size in the filename
                icon_path = app_path / (basename + extension)
                if icon_path.exists():
                    return icon_path

        elif file_extension.lower() in extensions:
            # If an icon *is* provided, it must be one of the acceptable types
            icon_path = app_path / self.filename
            if icon_path.exists():
                return icon_path
        else:
            # An icon has been specified, but it's not a valid format.
            raise FileNotFoundError(
                "{filename} is not a valid icon".format(
                    filename=self.filename
                )
            )

        raise FileNotFoundError(
            "Can't find icon {filename}".format(
                filename=self.filename
            )
        )


Icon.TOGA_ICON = Icon('resources/toga', system=True)
