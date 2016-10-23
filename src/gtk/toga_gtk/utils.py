import inspect

from gi.repository import GLib

from toga.constants import *


def long_running_task(task):
    try:
        delay = next(task)
        GLib.timeout_add_seconds(int(delay), long_running_task, task)
    except StopIteration:
        pass
    # Only iterate once; next iteration is internally queued
    return False


def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            result = handler(widget)
            if inspect.isgenerator(result):
                long_running_task(result)

    return _handler
