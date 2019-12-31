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
                self._impl = factory.Icon(interface=self)
            except FileNotFoundError:
                print("WARNING: Can't find icon {self.path}; falling back to default icon".format(
                    self=self
                ))
                self._impl = self.TOGA_ICON.bind(factory)

        return self._impl


Icon.TOGA_ICON = Icon('resources/toga', system=True)
