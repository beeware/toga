import weakref


class WeakrefCallable:  # pragma: no-cover-if-gtk3
    """
    A wrapper for callable that holds a weak reference to it.

    This can be useful in particular when setting gtk virtual function handlers,
    to avoid cyclical reference cycles between python and gi that are detected
    neither by the python garbage collector nor the gi.
    """

    def __init__(self, function):
        try:
            self.ref = weakref.WeakMethod(function)
        except TypeError:  # pragma: no cover
            self.ref = weakref.ref(function)

    def __call__(self, *args, **kwargs):
        function = self.ref()
        if function:  # pragma: no branch
            return function(*args, **kwargs)
