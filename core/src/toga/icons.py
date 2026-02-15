from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

import toga
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from typing import TypeAlias

    IconContentT: TypeAlias = str | Path | toga.Icon
    """
    When specifying an [Icon][], you can
    provide:

    - a string specifying an absolute or relative path;
    - an absolute or relative [`pathlib.Path`][]
      object; or
    - an instance of [`toga.Icon`][].

    If a relative path is provided, it will be anchored relative to the
    module that defines your Toga application class.
    """


class CachedIcon:
    def __init__(self, name: str, system: bool = False):
        """A wrapper that allows for deferred, cached Icon properties.

        :param name: The name of the icon to cache.
        :param system: Is the icon a system icon (i.e., one that is provided by Toga)
        """
        self.name = name
        self.system = system

    def __get__(self, obj: object, owner: type[Icon]) -> Icon:
        # If you ask for Icon.CACHED_ICON, obj is None, and owner is the Icon class
        # If you ask for self.CACHED_ICON, obj is self, from which we can get the class.
        cls = owner if obj is None else obj.__class__

        try:
            # Look for a __CACHED_ICON attribute on the class
            value = getattr(cls, f"_{self.name}")
        except AttributeError:
            value = Icon(self.name, system=self.system)
            setattr(cls, f"_{self.name}", value)
        return value


# A sentinel value that is type compatible with the `path` argument,
# but can be used to uniquely identify a request for an application icon
_APP_ICON = "<app icon>"


class Icon:
    APP_ICON = CachedIcon(_APP_ICON)
    """The application icon.

    The application icon will be loaded from `resources/<app name>` (where `<app
    name>` is the value of [`toga.App.app_name`][]).

    If this resource cannot be found, and the app has been packaged as a binary, the
    icon from the application binary will be used as a fallback.

    Otherwise, [`Icon.DEFAULT_ICON`][toga.Icon.DEFAULT_ICON] will be used.
    """

    DEFAULT_ICON = CachedIcon("toga", system=True)
    """The default icon used as a fallback - Toga's "Tiberius the yak" icon."""

    OPTION_CONTAINER_DEFAULT_TAB_ICON = CachedIcon("optioncontainer-tab", system=True)
    """The default icon used to decorate option container tabs."""

    def __init__(
        self,
        path: str | Path,
        *,
        system: bool = False,  # Deliberately undocumented; for internal use only
    ):
        """Create a new icon.

        :param path: Base filename for the icon. Should not contain an extension
            (If an extension is specified, it will be ignored). Paths can be absolute
            or relative. Relative paths start from the folder where your [`toga.App`][]
            subclass is defined.

            If the icon cannot be found, the default icon will be
            [Icon.DEFAULT_ICON][toga.Icon.DEFAULT_ICON].

            If icon is found, but cannot be loaded (due to a file format
            or permission error), a warning will be emitted and
            [Icon.DEFAULT_ICON][toga.Icon.DEFAULT_ICON] will be used.
        :param system: **For internal use only**
        """
        self.factory = get_platform_factory()
        try:
            # Try to load the icon with the given path snippet. If the request is for
            # the app icon, use `resources/<app name>` as the path.
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
        except (FileNotFoundError, ValueError) as exc:
            # Icon path couldn't be resolved or loaded. If the path is the sentinel
            # for the app icon, and this isn't running as a script, fall back to the
            # application binary.
            if path is _APP_ICON:
                if isinstance(exc, ValueError):
                    fallback = (
                        "application binary icon"
                        if toga.App.app.is_bundled
                        else "default icon"
                    )
                    print(
                        f"WARNING: Unable to load app icon {self.path}; "
                        f"falling back to {fallback}"
                    )
                if toga.App.app.is_bundled:
                    try:
                        # Use the application binary's icon
                        self._impl = self.factory.Icon(interface=self, path=None)
                    except (FileNotFoundError, ValueError):
                        # Can't find the application binary's icon.
                        print(
                            "WARNING: Can't find app icon; falling back to default icon"
                        )
                        self._impl = self.DEFAULT_ICON._impl
                else:
                    self._impl = self.DEFAULT_ICON._impl
            else:
                if isinstance(exc, FileNotFoundError):
                    print(
                        f"WARNING: Can't find icon {self.path}; "
                        f"falling back to default icon"
                    )
                else:
                    print(
                        f"WARNING: Unable to load icon {self.path}; "
                        f"falling back to default icon"
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
