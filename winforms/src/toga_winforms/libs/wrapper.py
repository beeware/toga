import weakref


class WeakrefCallable:
    """
    A wrapper for callable that holds a weak reference to it.

    This can be useful in particular when setting winforms event handlers, to avoid
    cyclical reference cycles between Python and the .NET CLR that are detected neither
    by the Python garbage collector nor the C# garbage collector.
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
