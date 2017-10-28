import asyncio
import weakref

__all__ = ['install', 'get_event_loop', 'wait_signal']


def install(gtk=False):
    """Set the default event loop policy.

    Call this as early as possible to ensure everything has a reference to the
    correct event loop.

    Set ``gtk`` to True if you intend to use Gtk in your application.

    If ``gtk`` is True and Gtk is not available, will raise `ValueError`.

    Note that this class performs some monkey patching of asyncio to ensure
    correct functionality.
    """

    if gtk:
        from .gtk import GtkEventLoopPolicy
        policy = GtkEventLoopPolicy()
    else:
        from .glib_events import GLibEventLoopPolicy
        policy = GLibEventLoopPolicy()

    # There are some libraries that use SafeChildWatcher directly (which is
    # completely reasonable), so we have to ensure that it is our version. I'm
    # sorry, I know this isn't great but it's basically the best that we have.
    from .glib_events import GLibChildWatcher
    asyncio.SafeChildWatcher = GLibChildWatcher
    asyncio.set_event_loop_policy(policy)


def get_event_loop():
    """Alias to asyncio.get_event_loop()."""
    return asyncio.get_event_loop()


class wait_signal(asyncio.Future):
    """A future for waiting for a given signal to occur."""

    def __init__(self, obj, name, *, loop=None):
        super().__init__(loop=loop)
        self._obj = weakref.ref(obj, lambda s: self.cancel())
        self._hnd = obj.connect(name, self._signal_callback)

    def _signal_callback(self, *k):
        obj = self._obj()
        if obj is not None:
            obj.disconnect(self._hnd)
        self.set_result(k)

    def cancel(self):
        if self.cancelled():
            return False
        super().cancel()
        obj = self._obj()
        if obj is not None:
            obj.disconnect(self._hnd)
        return True
