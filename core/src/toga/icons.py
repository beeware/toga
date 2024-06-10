from __future__ import annotations

import sys
import warnings
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import TYPE_CHECKING

import toga
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    if sys.version_info < (3, 10):
        from typing_extensions import TypeAlias
    else:
        from typing import TypeAlias

    IconContentT: TypeAlias = str | Path | toga.Icon


class cachedicon:
    def __init__(self, f: Callable[..., Icon]):
        self.f = f
        self.__doc__ = f.__doc__

    def __get__(self, obj: object, owner: type[Icon]) -> Icon:
        # If you ask for Icon.CACHED_ICON, obj is None, and owner is the Icon class
        # If you ask for self.CACHED_ICON, obj is self, from which we can get the class.
        cls = owner if obj is None else obj.__class__

        try:
            # Look for a __CACHED_ICON attribute on the class
            value = getattr(cls, f"__{self.f.__name__}")
        except AttributeError:
            value = self.f(owner)
            setattr(cls, f"__{self.f.__name__}", value)
        return value


# A sentinel value that is type compatible with the `path` argument,
# but can be used to uniquely identify a request for an application icon
_APP_ICON = "<app icon>"


class Icon:
    @cachedicon
    def TOGA_ICON(cls) -> Icon:
        """**DEPRECATED** - Use ``DEFAULT_ICON``, or your own icon."""
        warnings.warn(
            "TOGA_ICON has been deprecated; Use DEFAULT_ICON, or your own icon.",
            DeprecationWarning,
        )

        return Icon("toga", system=True)

    @cachedicon
    def APP_ICON(cls) -> Icon:
        """The application icon.

        The application icon will be loaded from ``resources/<app name>`` (where ``<app
        name>`` is the value of :attr:`toga.App.app_name`).

        If this resource cannot be found, and the app has been packaged as a binary, the
        icon from the application binary will be used as a fallback.

        Otherwise, :attr:`~toga.Icon.DEFAULT_ICON` will be used.
        """
        return Icon(_APP_ICON)

    @cachedicon
    def DEFAULT_ICON(cls) -> Icon:
        """The default icon used as a fallback - Toga's "Tiberius the yak" icon."""
        return Icon("toga", system=True)

    @cachedicon
    def OPTION_CONTAINER_DEFAULT_TAB_ICON(cls) -> Icon:
        """The default icon used to decorate option container tabs."""
        return Icon("optioncontainer-tab", system=True)

    def __init__(
        self,
        path: str | Path,
        *,
        system: bool = False,  # Deliberately undocumented; for internal use only
    ):
        """Create a new icon.

        :param path: Base filename for the icon. The path can be an absolute file system
            path, or a path relative to the module that defines your Toga application
            class. This base filename should *not* contain an extension. If an extension
            is specified, it will be ignored. If the icon cannot be found, the default
            icon will be :attr:`~toga.Icon.DEFAULT_ICON`. If an icon file is found, but
            it cannot be loaded (due to a file format or permission error), an exception
            will be raised.
        :param system: **For internal use only**
        """
        self.factory = get_platform_factory()
        try:
            # Try to load the icon with the given path snippet. If the request is for the
            # app icon, use ``resources/<app name>`` as the path.
            if path is _APP_ICON:
                self.path = Path(f"resources/{toga.App.app.app_name}")
            else:
                self.path = Path(path)

            self.system = system
            if self.system:
                resource_path = Path(self.factory.__file__).parent / "resources"
            else:
                resource_path = toga.App.app.paths.app

            full_path: dict[str, Path] | Path
            if self.factory.Icon.SIZES:
                full_path = {}
                for size in self.factory.Icon.SIZES:
                    try:
                        full_path[size] = self._full_path(
                            size=size,
                            extensions=self.factory.Icon.EXTENSIONS,
                            resource_path=resource_path,
                        )
                    except FileNotFoundError:
                        # This size variant wasn't found; we can skip it
                        pass
            else:
                full_path = self._full_path(
                    size=None,
                    extensions=self.factory.Icon.EXTENSIONS,
                    resource_path=resource_path,
                )

            self._impl = self.factory.Icon(interface=self, path=full_path)
        except FileNotFoundError:
            # Icon path couldn't be found. If the path is the sentinel for the app
            # icon, and this isn't running as a script, fall back to the application
            # binary
            if path is _APP_ICON:
                if toga.App.app.is_bundled:
                    try:
                        # Use the application binary's icon
                        self._impl = self.factory.Icon(interface=self, path=None)
                    except FileNotFoundError:
                        # Can't find the application binary's icon.
                        print(
                            "WARNING: Can't find app icon; falling back to default icon"
                        )
                        self._impl = self.DEFAULT_ICON._impl
                else:
                    self._impl = self.DEFAULT_ICON._impl
            else:
                print(
                    f"WARNING: Can't find icon {self.path}; falling back to default icon"
                )
                self._impl = self.DEFAULT_ICON._impl

    def _full_path(
        self,
        size: str | None,
        extensions: Iterable[str],
        resource_path: Path,
    ) -> Path:
        platform = toga.platform.current_platform
        if size:
            for extension in extensions:
                for filename in [
                    f"{self.path.stem}-{platform}-{size}{extension}",
                    f"{self.path.stem}-{size}{extension}",
                ]:
                    icon_path = resource_path / self.path.parent / filename
                    if icon_path.exists():
                        return icon_path

        # Look for size-less alternatives
        for extension in extensions:
            for filename in [
                f"{self.path.stem}-{platform}{extension}",
                f"{self.path.stem}{extension}",
            ]:
                icon_path = resource_path / self.path.parent / filename
                if icon_path.exists():
                    return icon_path

        raise FileNotFoundError(f"Can't find icon {self.path}")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Icon) and other._impl.path == self._impl.path
