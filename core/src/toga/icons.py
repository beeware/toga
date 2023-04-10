import os
import warnings

from toga.platform import get_platform_factory


class cachedicon:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        # If you ask for Icon.CACHED_ICON, obj is None, and owner is the Icon class
        # If you ask for self.CACHED_ICON, obj is self, from which we can get the class.
        if obj is None:
            cls = owner
        else:
            cls = obj.__class__

        try:
            # Look for a __CACHED_ICON attribute on the class
            value = getattr(cls, f"__{self.f.__name__}")
        except AttributeError:
            value = self.f(owner)
            setattr(cls, f"__{self.f.__name__}", value)
        return value


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

    @cachedicon
    def TOGA_ICON(cls):
        return Icon("resources/toga", system=True)

    @cachedicon
    def DEFAULT_ICON(cls):
        return Icon("resources/toga", system=True)

    def __init__(self, path, system=False):
        self.path = path
        self.system = system

        self.factory = get_platform_factory()
        try:
            if self.system:
                resource_path = self.factory.paths.toga
            else:
                resource_path = self.factory.paths.app

            if self.factory.Icon.SIZES:
                full_path = {
                    size: self._full_path(
                        size=size,
                        extensions=self.factory.Icon.EXTENSIONS,
                        resource_path=resource_path,
                    )
                    for size in self.factory.Icon.SIZES
                }
            else:
                full_path = self._full_path(
                    size=None,
                    extensions=self.factory.Icon.EXTENSIONS,
                    resource_path=resource_path,
                )

            self._impl = self.factory.Icon(interface=self, path=full_path)
        except FileNotFoundError:
            print(
                "WARNING: Can't find icon {self.path}; falling back to default icon".format(
                    self=self
                )
            )
            self._impl = Icon.DEFAULT_ICON._impl

    def bind(self, factory=None):
        warnings.warn(
            "Icons no longer need to be explicitly bound.", DeprecationWarning
        )
        return self._impl

    def _full_path(self, size, extensions, resource_path):
        basename, file_extension = os.path.splitext(self.path)

        if not file_extension:
            # If no extension is provided, look for one of the allowed
            # icon types, in preferred format order.
            for extension in extensions:
                icon_path = resource_path / f"{basename}-{size}{extension}"

                if icon_path.exists():
                    return icon_path

                # look for an icon file without a size in the filename
                icon_path = resource_path / f"{basename}{extension}"
                if icon_path.exists():
                    return icon_path

        elif file_extension.lower() in extensions:
            # If an icon *is* provided, it must be one of the acceptable types
            icon_path = resource_path / self.path
            if icon_path.exists():
                return icon_path
        else:
            # An icon has been specified, but it's not a valid format.
            raise FileNotFoundError(f"{self.path} is not a valid icon")

        raise FileNotFoundError(f"Can't find icon {self.path}")
