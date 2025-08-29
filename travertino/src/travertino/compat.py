from functools import cache
from importlib.metadata import PackageNotFoundError, metadata


@cache
def _toga_lt_5():
    try:
        toga_version = metadata("toga-core")["version"].split(".")
    except PackageNotFoundError:  # pragma: no cover
        # If Toga isn't installed at all, we shouldn't invoke the backwards
        # compatibility shim; any exceptions must be from other sources.
        return False
    else:
        return [int(v) for v in toga_version[:2]] < (0, 5)
