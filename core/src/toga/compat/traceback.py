# TODO: update the PyScript build to include this module from micropython-lib.

import sys

__all__ = [
    "format_tb",
    "format_exception_only",
    "format_exception",
    "print_exception",
    "print_exc",
    "format_exc",
]


def format_tb(tb, limit):
    return ["traceback.format_tb() not implemented\n"]


def format_exception_only(type, value):
    return [repr(value) + "\n"]


def format_exception(etype, value, tb, limit=None, chain=True):
    return format_exception_only(etype, value)


def print_exception(t, e, tb, limit=None, file=None, chain=True):
    if file is None:
        file = sys.stdout
    sys.print_exception(e, file)


def print_exc(limit=None, file=None, chain=True):
    print_exception(*sys.exc_info(), limit=limit, file=file, chain=chain)


def format_exc(limit=None, chain=True):
    return "".join(format_exception(*sys.exc_info(), limit=limit, chain=chain))
