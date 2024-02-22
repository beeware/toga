from __future__ import annotations

import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING

import toga
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    if sys.version_info < (3, 10):
        from typing_extensions import TypeAlias
    else:
        from typing import TypeAlias

    IconContent: TypeAlias = str | Path | toga.Icon


class cachedicon:
    def __init__(self, f):
        self.f = f
        self.__doc__ = f.__doc__

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
    @cachedicon
    def TOGA_ICON(cls) -> Icon:
        """**DEPRECATED** - Use ``DEFAULT_ICON``, or your own icon."""
        warnings.warn(
            "TOGA_ICON has been deprecated; Use DEFAULT_ICON, or your own icon.",
            DeprecationWarning,
        )

        return Icon("toga", system=True)

    @cachedicon
    def DEFAULT_ICON(cls) -> Icon:
        """The default icon used as a fallback."""
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
            class.

            This base filename should *not* contain an extension. If an extension is
            specified, it will be ignored.
        :param system: **For internal use only**
        """
        self.path = Path(path)
        self.system = system

        self.factory = get_platform_factory()
        try:
            if self.system:
                resource_path = Path(self.factory.__file__).parent / "resources"
            else:
                resource_path = toga.App.app.paths.app

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
            print(f"WARNING: Can't find icon {self.path}; falling back to default icon")
            self._impl = self.DEFAULT_ICON._impl

    def _full_path(self, size, extensions, resource_path):
        platform = toga.platform.current_platform
        for extension in extensions:
            for filename in (
                [
                    f"{self.path.stem}-{platform}-{size}{extension}",
                    f"{self.path.stem}-{size}{extension}",
                ]
                if size
                else []
            ) + [
                f"{self.path.stem}-{platform}{extension}",
                f"{self.path.stem}{extension}",
            ]:
                icon_path = resource_path / self.path.parent / filename
                if icon_path.exists():
                    return icon_path

        raise FileNotFoundError(f"Can't find icon {self.path}")
