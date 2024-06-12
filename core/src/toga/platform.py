from __future__ import annotations

import importlib
import os
import sys
from functools import lru_cache
from types import ModuleType

if sys.version_info >= (3, 10):  # pragma: no-cover-if-lt-py310
    from importlib.metadata import entry_points
else:  # pragma: no-cover-if-gte-py310
    # Before Python 3.10, entry_points did not support the group argument;
    # so, the backport package must be used on older versions.
    from importlib_metadata import entry_points


# Map python sys.platform with toga platforms names
_TOGA_PLATFORMS = {
    "android": "android",
    "darwin": "macOS",
    "ios": "iOS",
    "linux": "linux",
    "freebsd": "freeBSD",
    "tvos": "tvOS",
    "watchos": "watchOS",
    "wearos": "wearOS",
    "emscripten": "web",
    "win32": "windows",
}


def get_current_platform() -> str | None:
    # Rely on `sys.getandroidapilevel`, which only exists on Android; see
    # https://github.com/beeware/Python-Android-support/issues/8
    if hasattr(sys, "getandroidapilevel"):
        return "android"
    elif sys.platform.startswith("freebsd"):
        return "freeBSD"
    else:
        return _TOGA_PLATFORMS.get(sys.platform)


current_platform = get_current_platform()


def find_backends():
    # As of Setuptools 65.5, entry points are returned duplicated if the
    # package is installed editable. Use a set to ensure that each entry point
    # is only returned once.
    # See https://github.com/pypa/setuptools/issues/3649
    return sorted(set(entry_points(group="toga.backends")))


@lru_cache(maxsize=1)
def get_platform_factory() -> ModuleType:
    """Determine the current host platform and import the platform factory.

    If the ``TOGA_BACKEND`` environment variable is set, the factory will be loaded
    from that module.

    Raises :any:`RuntimeError` if an appropriate host platform cannot be identified.

    :returns: The factory for the host platform.
    """
    if backend_value := os.environ.get("TOGA_BACKEND"):
        try:
            factory = importlib.import_module(f"{backend_value}.factory")
        except ModuleNotFoundError as e:
            toga_backends_values = ", ".join(
                [f"{backend.value!r}" for backend in find_backends()]
            )
            # Android doesn't report Python exception chains in crashes
            # (https://github.com/chaquo/chaquopy/issues/890), so include the original
            # exception message in case the backend does exist but throws a
            # ModuleNotFoundError from one of its internal imports.
            raise RuntimeError(
                f"The backend specified by TOGA_BACKEND ({backend_value!r}) could "
                f"not be loaded ({e}). It should be one of: {toga_backends_values}."
            )
    else:
        toga_backends = find_backends()
        if len(toga_backends) == 0:
            raise RuntimeError("No Toga backend could be loaded.")
        elif len(toga_backends) == 1:
            backend = toga_backends[0]
        else:
            # multiple backends are installed: choose the one that matches the host platform
            matching_backends = [
                backend for backend in toga_backends if backend.name == current_platform
            ]
            if len(matching_backends) == 0:
                toga_backends_string = ", ".join(
                    [f"{backend.value!r} ({backend.name})" for backend in toga_backends]
                )
                raise RuntimeError(
                    f"Multiple Toga backends are installed ({toga_backends_string}), "
                    f"but none of them match your current platform ({current_platform!r}). "
                    "Install a backend for your current platform, or use "
                    "TOGA_BACKEND to specify a backend."
                )
            if len(matching_backends) > 1:
                toga_backends_string = ", ".join(
                    [
                        f"{backend.value!r} ({backend.name})"
                        for backend in matching_backends
                    ]
                )
                raise RuntimeError(
                    f"Multiple candidate toga backends found: ({toga_backends_string}). "
                    "Uninstall the backends you don't require, or use "
                    "TOGA_BACKEND to specify a backend."
                )
            backend = matching_backends[0]
        factory = importlib.import_module(f"{backend.value}.factory")
    return factory
