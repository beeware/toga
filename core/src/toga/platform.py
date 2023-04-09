import importlib
import os
import sys
import warnings
from functools import lru_cache

try:
    # Usually, the pattern is "import module; if it doesn't exist,
    # import the shim". However, we need the 3.10 API for entry_points,
    # as the 3.8 didn't support the `groups` argument to entry_points.
    # Therefore, we try to import the compatibility shim first; and fall
    # back to the stdlib module if the shim isn't there.
    from importlib_metadata import entry_points
except ImportError:
    from importlib.metadata import entry_points


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


try:
    current_platform = os.environ["TOGA_PLATFORM"]
except KeyError:
    # Rely on `sys.getandroidapilevel`, which only exists on Android; see
    # https://github.com/beeware/Python-Android-support/issues/8
    if hasattr(sys, "getandroidapilevel"):
        current_platform = "android"
    elif sys.platform.startswith("freebsd"):
        current_platform = "freeBSD"
    else:
        current_platform = _TOGA_PLATFORMS.get(sys.platform)


@lru_cache(maxsize=1)
def get_platform_factory(factory=None):
    """This function figures out what the current host platform is and imports
    the adequate factory. The factory is the interface to all platform specific
    implementations.

    If the TOGA_BACKEND environment variable is set, the factory will be loaded
    from that module.

    Returns: The suitable factory for the current host platform.

    Raises:
        RuntimeError: If no supported host platform can be identified.
    """

    ######################################################################
    # 2022-09: Backwards compatibility
    ######################################################################
    # factory no longer used
    if factory:
        warnings.warn("The factory argument is no longer used.", DeprecationWarning)
    ######################################################################
    # End backwards compatibility.
    ######################################################################

    toga_backends = entry_points(group="toga.backends")
    if not toga_backends:
        raise RuntimeError("No Toga backend could be loaded.")

    backend_value = os.environ.get("TOGA_BACKEND")
    if backend_value:
        try:
            factory = importlib.import_module(f"{backend_value}.factory")
        except ModuleNotFoundError:
            toga_backends_values = ", ".join(
                [f"{backend.value!r}" for backend in toga_backends]
            )
            raise RuntimeError(
                f"The backend specified by TOGA_BACKEND ({backend_value!r}) "
                f"could not be loaded. It should be one of: {toga_backends_values}."
            )
    else:
        # As of Setuptools 65.5, entry points are returned duplicated if the
        # package is installed editable. Use a set to ensure that each entry point
        # is only returned once.
        # See https://github.com/pypa/setuptools/issues/3649
        toga_backends = sorted(set(toga_backends))

        if len(toga_backends) == 1:
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
                    f"but none of them match your current platform ({current_platform!r})."
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
