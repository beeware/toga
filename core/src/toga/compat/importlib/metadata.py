import sys

__all__ = ["entry_points", "metadata", "version"]


def entry_points():
    return {} if sys.version < (3, 10) else []


def metadata(distribution_name):
    return {}


# Return None so it'll work if it's simply assigned to a __version__ attribute, but will
# give an error if it's ever used for anything else.
def version(distribution_name):
    return None
