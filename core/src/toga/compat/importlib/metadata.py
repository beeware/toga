import sys

__all__ = ["entry_points", "metadata", "version"]


def entry_points():
    return {} if sys.version < (3, 10) else []


def metadata(distribution_name):
    return {}


class PackageNotFoundError(Exception):
    pass


def version(distribution_name):
    raise PackageNotFoundError(distribution_name)
