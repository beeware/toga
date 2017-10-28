"""PEP 3156 event loop based on GLib"""

import os
import signal
import threading
from asyncio import events, tasks, unix_events

from gi.repository import GLib, Gio

__all__ = ['GLibEventLoop', 'GLibEventLoopPolicy']


class GLibChildWatcher(unix_events.AbstractChildWatcher):
    def __init__(self):
        self._sources = {}

    def attach_loop(self, loop):
        # just ignored
        pass

    def add_child_handler(self, pid, callback, *args):
        self.remove_child_handler(pid)

        source = GLib.child_watch_add(0, pid, self.__callback__)
        self._sources[pid] = source, callback, args

    def remove_child_handler(self, pid):
        try:
            source = self._sources.pop(pid)[0]
        except KeyError:
            return False

        GLib.source_remove(source)
        return True

    def close(self):
        for source, callback, args in self._sources.values():
            GLib.source_remove(source)

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass

    def __callback__(self, pid, status):

        try:
            source, callback, args = self._sources.pop(pid)
        except KeyError:
            return

        GLib.source_remove(source)

        if os.WIFSIGNALED(status):
            returncode = -os.WTERMSIG(status)
        elif os.WIFEXITED(status):
            returncode = os.WEXITSTATUS(status)

            #FIXME: Hack for adjusting invalid status returned by GLIB
            #    Looks like there is a bug in glib or in pygobject
            if returncode > 128:
                returncode = 128 - returncode
        else:
            returncode = status

        callback(pid, returncode, *args)


class GLibHandle(events.Handle):
    __slots__ = ('_source', '_repeat')

    def __init__(self, *, loop, source, repeat, callback, args):
        super().__init__(callback, args, loop)

        self._source = source
        self._repeat = repeat
        loop._handlers.add(self)
        source.set_callback(self.__callback__, self)
        source.attach(loop._context)

    def cancel(self):
        super().cancel()
        self._source.destroy()
        self._loop._handlers.discard(self)

    def __callback__(self, ignore_self):
        # __callback__ is called within the MainContext object, which is
        # important in case that code includes a `Gtk.main()` or some such.
        # Otherwise what happens is the loop is started recursively, but the
        # callbacks don't finish firing, so they can't be rescheduled.
        self._run()
        if not self._repeat:
            self._source.destroy()
            self._loop._handlers.discard(self)

        return self._repeat


class BaseGLibEventLoop(unix_events.SelectorEventLoop):
    """GLib base event loop

    This class handles only the operations related to Glib.MainContext objects.

    Glib.MainLoop operations are implemented in the derived classes.
    """

    def __init__(self):
        self._readers = {}
        self._writers = {}
        self._sighandlers = {}
        self._chldhandlers = {}
        self._handlers = set()

        super().__init__()

    def run_until_complete(self, future, **kw):
        """Run the event loop until a Future is done.

        Return the Future's result, or raise its exception.
        """

        def stop(f):
            self.stop()

        future = tasks.async(future, loop=self)
        future.add_done_callback(stop)
        try:
            self.run_forever(**kw)
        finally:
            future.remove_done_callback(stop)

        if not future.done():
            raise RuntimeError('Event loop stopped before Future completed.')

        return future.result()

    def run_forever(self):
        """Run the event loop until stop() is called."""
        if self.is_running():
            raise RuntimeError(
                "Recursively calling run_forever is forbidden. "
                "To recursively run the event loop, call run().")

        try:
            self.run()
        finally:
            self.stop()

    def is_running(self):
        """Return whether the event loop is currently running."""
        return self._running

    def stop(self):
        """Stop the event loop as soon as reasonable.

        Exactly how soon that is may depend on the implementation, but
        no more I/O callbacks should be scheduled.
        """
        raise NotImplementedError()  # pragma: no cover

    def close(self):
        for fd in list(self._readers):
            self._remove_reader(fd)

        for fd in list(self._writers):
            self.remove_writer(fd)

        for sig in list(self._sighandlers):
            self.remove_signal_handler(sig)

        for pid in list(self._chldhandlers):
            self._remove_child_handler(pid)

        for s in list(self._handlers):
            s.cancel()

        super().close()

    def _check_not_coroutine(self, callback, name):
        from asyncio import coroutines
        if (coroutines.iscoroutine(callback) or
                coroutines.iscoroutinefunction(callback)):
            raise TypeError("coroutines cannot be used with {}()".format(name))

    # Methods scheduling callbacks.  All these return Handles.
    def call_soon(self, callback, *args):
        self._check_not_coroutine(callback, 'call_soon')
        source = GLib.Idle()

        # XXX: we set the source's priority to high for the following scenario:
        #
        # - loop.sock_connect() begins asynchronous connection
        # - this adds a write callback to detect when the connection has
        #   completed
        # - this write callback sets the result of a future
        # - future.Future schedules callbacks with call_later.
        # - the callback for this future removes the write callback
        # - GLib.Idle() has a much lower priority than that of the GSource for
        #   the writer, so it never gets scheduled.
        source.set_priority(GLib.PRIORITY_HIGH)

        return GLibHandle(
            loop=self,
            source=source,
            repeat=False,
            callback=callback,
            args=args)

    call_soon_threadsafe = call_soon

    def call_later(self, delay, callback, *args):
        self._check_not_coroutine(callback, 'call_later')

        return GLibHandle(
            loop=self,
            source=GLib.Timeout(delay*1000) if delay > 0 else GLib.Idle(),
            repeat=False,
            callback=callback,
            args=args)

    def call_at(self, when, callback, *args):
        self._check_not_coroutine(callback, 'call_at')

        return self.call_later(when - self.time(), callback, *args)

    def time(self):
        return GLib.get_monotonic_time() / 1000000

    # FIXME: these functions are not available on windows
    def _add_reader(self, fd, callback, *args):
        if not isinstance(fd, int):
            fd = fd.fileno()

        self._remove_reader(fd)

        s = GLib.unix_fd_source_new(fd, GLib.IO_IN)

        assert fd not in self._readers
        self._readers[fd] = GLibHandle(
            loop=self,
            source=s,
            repeat=True,
            callback=callback,
            args=args)

    def _remove_reader(self, fd):
        if not isinstance(fd, int):
            fd = fd.fileno()

        try:
            self._readers.pop(fd).cancel()
            return True

        except KeyError:
            return False

    def _add_writer(self, fd, callback, *args):
        if not isinstance(fd, int):
            fd = fd.fileno()

        self._remove_writer(fd)

        s = GLib.unix_fd_source_new(fd, GLib.IO_OUT)

        assert fd not in self._writers

        self._writers[fd] = GLibHandle(
            loop=self,
            source=s,
            repeat=True,
            callback=callback,
            args=args)

    def _remove_writer(self, fd):
        if not isinstance(fd, int):
            fd = fd.fileno()

        try:
            self._writers.pop(fd).cancel()
            return True

        except KeyError:
            return False

    # Disgusting backwards compatibility hack to ensure gbulb keeps working
    # with Python versions that don't have http://bugs.python.org/issue28369
    if not hasattr(unix_events.SelectorEventLoop, '_add_reader'):
        add_reader = _add_reader
        add_writer = _add_writer
        remove_writer = _remove_writer
        remove_reader = _remove_reader

    # Signal handling.

    def add_signal_handler(self, sig, callback, *args):
        self._check_signal(sig)
        self.remove_signal_handler(sig)

        s = GLib.unix_signal_source_new(sig)
        if s is None:
            if sig == signal.SIGKILL:
                raise RuntimeError("cannot catch SIGKILL")
            else:
                raise ValueError("signal not supported")

        assert sig not in self._sighandlers

        self._sighandlers[sig] = GLibHandle(
            loop=self,
            source=s,
            repeat=True,
            callback=callback,
            args=args)

    def remove_signal_handler(self, sig):
        self._check_signal(sig)
        try:
            self._sighandlers.pop(sig).cancel()
            return True

        except KeyError:
            return False


class GLibEventLoop(BaseGLibEventLoop):
    def __init__(self, *, context=None, application=None):
        self._context = context or GLib.MainContext()
        self._application = application
        self._running = False

        if application is None:
            self._mainloop = GLib.MainLoop(self._context)
        super().__init__()

    def run(self):
        recursive = self.is_running()

        self._running = True
        try:
            if self._application is not None:
                self._application.run(None)
            else:
                self._mainloop.run()
        finally:
            if not recursive:
                self._running = False

    def stop(self):
        """Stop the inner-most invocation of the event loop.

        Typically, this will mean stopping the event loop completely.

        Note that due to the nature of GLib's main loop, stopping may not be
        immediate.
        """

        if self._application is not None:
            self._application.quit()
        else:
            self._mainloop.quit()

    def run_forever(self, application=None):
        """Run the event loop until stop() is called."""

        if application is not None:
            self.set_application(application)
        super().run_forever()

    def set_application(self, application):
        if not isinstance(application, Gio.Application):
            raise TypeError("application must be a Gio.Application object")
        if self._application is not None:
            raise ValueError("application is already set")
        if self.is_running():
            raise RuntimeError("You can't add the application to a loop that's already running.")
        self._application = application
        self._policy._application = application
        del self._mainloop


class GLibEventLoopPolicy(events.AbstractEventLoopPolicy):
    """Default GLib event loop policy

    In this policy, each thread has its own event loop.  However, we only
    automatically create an event loop by default for the main thread; other
    threads by default have no event loop.
    """

    #TODO add a parameter to synchronise with GLib's thread default contexts
    #   (g_main_context_push_thread_default())
    def __init__(self, application=None):
        self._default_loop = None
        self._application = application
        self._watcher_lock = threading.Lock()

        self._watcher = None
        self._policy = unix_events.DefaultEventLoopPolicy()
        self._policy.new_event_loop = self.new_event_loop
        self.get_event_loop = self._policy.get_event_loop
        self.set_event_loop = self._policy.set_event_loop

    def get_child_watcher(self):
        if self._watcher is None:
            with self._watcher_lock:
                if self._watcher is None:
                    self._watcher = GLibChildWatcher()
        return self._watcher

    def set_child_watcher(self, watcher):
        """Set a child watcher.

        Must be an an instance of GLibChildWatcher, as it ties in with GLib
        appropriately.
        """

        if watcher is not None and not isinstance(watcher, GLibChildWatcher):
            raise TypeError("Only GLibChildWatcher is supported!")

        with self._watcher_lock:
            self._watcher = watcher

    def new_event_loop(self):
        """Create a new event loop and return it."""
        if not self._default_loop and isinstance(threading.current_thread(), threading._MainThread):
            l = self.get_default_loop()
        else:
            l = GLibEventLoop()
        l._policy = self

        return l

    def get_default_loop(self):
        """Get the default event loop."""
        if not self._default_loop:
            self._default_loop = self._new_default_loop()
        return self._default_loop

    def _new_default_loop(self):
        l = GLibEventLoop(
            context=GLib.main_context_default(), application=self._application)
        l._policy = self
        return l
