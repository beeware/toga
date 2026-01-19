from __future__ import annotations

import importlib
import os
import sys
from functools import cache
from importlib.metadata import entry_points
from types import ModuleType

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


current_platform: str = get_current_platform()
"""A string identifier of the platform on which the application is currently running.
One of:

* `android`
* `macOS`
* `iOS`
* `linux`
* `freeBSD`
* `web`
* `windows`

**DEPRECATED**: This property exists for historical reasons. On Python 3.13 and later,
you can use the Python standard library property [`sys.platform`][].

It is required on Python 3.12 and earlier because Android historically returned
`sys.platform == "linux"` until the `android` value was formalied by PEP 783. The names
used by `current_platform` do not exactly match the names returned by
[`sys.platform`][].
"""


def find_backends():
    # As of Setuptools 65.5, entry points are returned duplicated if the
    # package is installed editable. Use a set to ensure that each entry point
    # is only returned once.
    # See https://github.com/pypa/setuptools/issues/3649
    return sorted(set(entry_points(group="toga.backends")))


@cache
def get_platform_factory() -> ModuleType:
    """Determine the current host platform and import the platform factory.

    If the `TOGA_BACKEND` environment variable is set, the factory will be loaded
    from that module.

    Raises [`RuntimeError`][] if an appropriate host platform cannot be identified.

    :returns: The factory for the host platform.
    """
    if backend_value := os.environ.get("TOGA_BACKEND"):
        try:
            factory = importlib.import_module(f"{backend_value}.factory")
        except ModuleNotFoundError as exc:
            toga_backends_values = ", ".join(
                [f"{backend.value!r}" for backend in find_backends()]
            )
            # Android doesn't report Python exception chains in crashes
            # (https://github.com/chaquo/chaquopy/issues/890), so include the original
            # exception message in case the backend does exist but throws a
            # ModuleNotFoundError from one of its internal imports.
            raise RuntimeError(
                f"The backend specified by TOGA_BACKEND ({backend_value!r}) could "
                f"not be loaded ({exc}). It should be one of: {toga_backends_values}."
            ) from exc

    else:
        toga_backends = find_backends()
        if len(toga_backends) == 0:
            raise RuntimeError("No Toga backend could be loaded.")
        elif len(toga_backends) == 1:
            backend = toga_backends[0]
        else:
            # multiple backends are installed: choose the one that
            # matches the host platform
            matching_backends = [
                backend for backend in toga_backends if backend.name == current_platform
            ]
            if len(matching_backends) == 0:
                toga_backends_string = ", ".join(
                    [f"{backend.value!r} ({backend.name})" for backend in toga_backends]
                )
                raise RuntimeError(
                    f"Multiple Toga backends are installed ({toga_backends_string}), "
                    f"but none of them match your current platform "
                    f"({current_platform!r}). "
                    f"Install a backend for your current platform, or use "
                    f"TOGA_BACKEND to specify a backend."
                )
            if len(matching_backends) > 1:
                toga_backends_string = ", ".join(
                    [
                        f"{backend.value!r} ({backend.name})"
                        for backend in matching_backends
                    ]
                )
                raise RuntimeError(
                    f"Multiple candidate toga backends found: "
                    f"({toga_backends_string}). "
                    f"Uninstall the backends you don't require, or use "
                    f"TOGA_BACKEND to specify a backend."
                )
            backend = matching_backends[0]
        factory = importlib.import_module(f"{backend.value}.factory")
    return factory


backend: str
"""The name of the backend that is being used by Toga to implement
platform-specific capabilities (e.g., `toga_cocoa`, `toga_gtk`).
"""


def __getattr__(name):
    if name == "backend":
        global backend
        backend = get_platform_factory().__package__
        return backend
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
