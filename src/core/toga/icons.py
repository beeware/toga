import os


class Icon:
    """
    A representation of an Icon image.

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

        # Resource is late bound.
        self._impl = None

    def bind(self, factory):
        """
        Bind the Icon to a factory.

        Creates the underlying platform implemenation of the Icon. If the
        image cannot be found, it will fall back to the default icon.

        :param factory: The platform factory to bind to.
        :returns: The platform implementation
        """
        if self._impl is None:
            try:
                if self.system:
                    resource_path = factory.paths.toga
                else:
                    resource_path = factory.paths.app

                if factory.Icon.SIZES:
                    full_path = {
                        size: self._full_path(
                            size=size,
                            extensions=factory.Icon.EXTENSIONS,
                            resource_path=resource_path,
                        )
                        for size in factory.Icon.SIZES
                    }
                else:
                    full_path = self._full_path(
                        size=None,
                        extensions=factory.Icon.EXTENSIONS,
                        resource_path=resource_path,
                    )

                self._impl = factory.Icon(interface=self, path=full_path)
            except FileNotFoundError:
                print("WARNING: Can't find icon {self.path}; falling back to default icon".format(
                    self=self
                ))
                self._impl = self.DEFAULT_ICON.bind(factory)

        return self._impl

    def _full_path(self, size, extensions, resource_path):
        basename, file_extension = os.path.splitext(self.path)

        if not file_extension:
            # If no extension is provided, look for one of the allowed
            # icon types, in preferred format order.
            for extension in extensions:
                # look for an icon file with a size in the filename
                icon_path = resource_path / (
                    '{basename}-{size}{extension}'.format(
                        basename=basename,
                        size=size,
                        extension=extension
                    )
                )
                if icon_path.exists():
                    return icon_path

                # look for a icon file without a size in the filename
                icon_path = resource_path / (basename + extension)
                if icon_path.exists():
                    return icon_path

        elif file_extension.lower() in extensions:
            # If an icon *is* provided, it must be one of the acceptable types
            icon_path = resource_path / self.path
            if icon_path.exists():
                return icon_path
        else:
            # An icon has been specified, but it's not a valid format.
            raise FileNotFoundError(
                "{self.path} is not a valid icon".format(
                    self=self
                )
            )

        raise FileNotFoundError(
            "Can't find icon {self.path}".format(
                self=self
            )
        )


Icon.TOGA_ICON = Icon('resources/toga', system=True)
Icon.DEFAULT_ICON = Icon('resources/toga', system=True)
