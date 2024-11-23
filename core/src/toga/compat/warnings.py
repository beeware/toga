# TODO: update the PyScript build to include this module from micropython-lib.

__all__ = ["filterwarnings", "warn"]


def filterwarnings(*args, **kwargs):
    pass


def warn(msg, cat=None, stacklevel=1):
    print("{}: {}".format("Warning" if cat is None else cat.__name__, msg))
