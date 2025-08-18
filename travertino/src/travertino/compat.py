from functools import cache
from importlib.metadata import PackageNotFoundError, metadata

from packaging.version import Version


@cache
def _toga_lt_5():
    try:
        toga_version = Version(metadata("toga-core")["version"])
    except PackageNotFoundError:  # pragma: no cover
        # If Toga isn't installed at all, we shouldn't invoke the backwards
        # compatibility shim; any exceptions must be from other sources.
        return False
    else:
        return toga_version < Version("0.5.0")
