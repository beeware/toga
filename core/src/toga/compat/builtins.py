__all__ = [
    "DeprecationWarning",
    "FileNotFoundError",
    "ModuleNotFoundError",
    "RuntimeWarning",
    "Warning",
]


# Alias missing exception classes to their superclasses so they'll still work in
# `except` statements.
FileNotFoundError = OSError
ModuleNotFoundError = ImportError


# Inherit from the stdlib Warning class if it exists.
try:
    Warning
except NameError:

    class Warning(Exception):
        pass


class DeprecationWarning(Warning):
    pass


class RuntimeWarning(Warning):
    pass
