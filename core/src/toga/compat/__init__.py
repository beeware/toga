# This package contains compatibility shims for alternative Python implementations,
# primarily MicroPython. Each of its modules corresponds to a standard library module.

import os
import re
import sys
from os.path import dirname, exists, isdir

from .importlib import import_module


def process_module(mod_name):
    if not mod_name:
        # Top-level compatibility package, i.e. this file.
        compat_mod = import_module(__name__)
    else:
        compat_mod = import_module(f"{__name__}.{mod_name}")
        try:
            stdlib_mod = import_module(mod_name)
        except ImportError:
            # The module doesn't exist in the standard library, so put the compatibility
            # module in its place.
            sys.modules[mod_name] = compat_mod
        else:
            # The module does exist in the standard library. Augment it with any missing
            # attributes.
            for attr in compat_mod.__all__:
                if not hasattr(stdlib_mod, attr):
                    setattr(stdlib_mod, attr, getattr(compat_mod, attr))

    # Recurse into packages.
    if hasattr(compat_mod, "__path__"):
        package_dir = dirname(compat_mod.__file__)
        package_prefix = f"{mod_name}." if mod_name else ""
        for filename in os.listdir(package_dir):
            path = f"{package_dir}/{filename}"
            if isdir(path) and exists(f"{path}/__init__.py"):
                process_module(f"{package_prefix}{filename}")
            elif (
                match := re.search(r"^(.+)\.py$", filename)
            ) and path != compat_mod.__file__:
                process_module(f"{package_prefix}{match.group(1)}")


if sys.implementation.name != "cpython":
    process_module(None)
