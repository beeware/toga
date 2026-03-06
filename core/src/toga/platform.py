from __future__ import annotations

import importlib
import os
import sys
import warnings
from functools import cache, cached_property
from importlib.metadata import entry_points
from types import ModuleType

from . import NotImplementedWarning

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

# Official Toga interface entry-point groups.
_TOGA_INTERFACES = {"toga_core"}


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
def get_backend():
    if (backend := os.environ.get("TOGA_BACKEND")) is None:
        toga_backends = find_backends()
        if len(toga_backends) == 0:
            raise RuntimeError("No Toga backend could be found.")
        elif len(toga_backends) == 1:
            backend = toga_backends[0].value
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
            backend = matching_backends[0].value
    return backend


@cache
def get_platform_factory() -> ModuleType:
    """Determine the current host platform and import the platform factory.

    **DEPRECATED**: Use get_factory() and entry points instead of factory modules.

    If the `TOGA_BACKEND` environment variable is set, the factory will be loaded
    from that module.

    Raises [`RuntimeError`][] if an appropriate host platform cannot be identified.

    :returns: The factory for the host platform.
    """
    warnings.warn(
        "The 'get_platform_factory' function is deprecated, use 'get_factory' instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    backend = get_backend()
    try:
        factory = importlib.import_module(f"{backend}.factory")
    except ModuleNotFoundError as exc:  # pragma: no cover
        # This is difficult to test now that it is not used directly.
        toga_backends_values = ", ".join([f"{b.value!r}" for b in find_backends()])
        # Android doesn't report Python exception chains in crashes
        # (https://github.com/chaquo/chaquopy/issues/890), so include the original
        # exception message in case the backend does exist but throws a
        # ModuleNotFoundError from one of its internal imports.
        raise RuntimeError(
            f"The backend specified by TOGA_BACKEND ({backend!r}) could "
            f"not be loaded ({exc}). It should be one of: {toga_backends_values}."
        ) from exc
    return factory


class Factory:
    """An object that lazily loads backend implementations from entry points."""

    def __init__(self, interface=None):
        if interface is None:
            self.interface = "toga_core"
        else:
            if interface.startswith("toga_") and interface not in _TOGA_INTERFACES:
                warnings.warn(
                    f"Unrecognized official Toga interface '{interface}'. "
                    "Third party interface names should start with 'togax_'",
                    RuntimeWarning,
                    stacklevel=2,
                )
            elif not interface.startswith("togax_"):
                warnings.warn(
                    "Third party interface names should start with 'togax_'",
                    RuntimeWarning,
                    stacklevel=2,
                )
            self.interface = interface
        self._entrypoints = None

    @cached_property
    def backend(self) -> str:
        return get_backend()

    @cached_property
    def group(self) -> str:
        return f"{self.interface}.backend.{self.backend}"

    def not_implemented(self, feature):
        NotImplementedWarning.warn(self.backend, feature)

    def _load_entrypoints(self):
        self._entrypoints = {}
        for entrypoint in entry_points(group=self.group):
            if entrypoint.name in self._entrypoints:  # pragma: no cover
                # can't test this in core tests
                other = self._entrypoints[entrypoint.name]
                warnings.warn(
                    f"Entrypoint {entrypoint.name!r} is defined multiple times in "
                    f"group {self.group}: {other.value} and {entrypoint.value}. "
                    "The first will be used.",
                    RuntimeWarning,
                    stacklevel=2,
                )
            else:
                self._entrypoints[entrypoint.name] = entrypoint

    def __getattr__(self, name):
        if self._entrypoints is None:
            self._load_entrypoints()
        if name in self._entrypoints:
            value = self._entrypoints[name].load()
            setattr(self, name, value)
            return value
        else:
            raise NotImplementedError(
                f"The {self.backend!r} backend for the {self.interface} interface "
                f"doesn't implement {name}"
            )


@cache
def get_factory(interface: str | None = None) -> Factory | ModuleType:
    """Return the implementation factory for an interface group.

    The object that is returned is a namespace whose attributes are the
    implementation classes for the current backend contributed by the
    appropriate entry points.

    :param interface: the name of the interface group for the factory, or None
        for the default `"toga_core"` interface.  Third-party interface group
        names should start with `"togax_"`.
    :returns: The factory namespace object.
    """
    factory = Factory(interface)
    # -------------------------------------------------------------------------
    # 2026-02: Backwards compatibility for version <= 0.5.3
    # -------------------------------------------------------------------------
    # If we can't find the entrypoint group we expect, drop back to the old
    # system using a factory module
    if interface is None and len(entry_points(group=factory.group)) == 0:
        backend = get_backend()
        try:
            factory = importlib.import_module(f"{backend}.factory")
        except ModuleNotFoundError as exc:
            toga_backends_values = ", ".join([f"{b.value!r}" for b in find_backends()])
            # Android doesn't report Python exception chains in crashes
            # (https://github.com/chaquo/chaquopy/issues/890), so include the original
            # exception message in case the backend does exist but throws a
            # ModuleNotFoundError from one of its internal imports.
            raise RuntimeError(
                f"The backend specified by TOGA_BACKEND ({backend!r}) could "
                f"not be loaded ({exc}). It should be one of: {toga_backends_values}."
            ) from exc
    # -------------------------------------------------------------------------
    # End backwards compatibility
    # -------------------------------------------------------------------------
    return factory


backend: str
"""The name of the backend that is being used by Toga to implement
platform-specific capabilities (e.g., `toga_cocoa`, `toga_gtk`).
"""


def __getattr__(name):
    if name == "backend":
        global backend
        backend = get_backend()
        return backend
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'") from None
