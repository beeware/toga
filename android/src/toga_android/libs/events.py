import asyncio
import asyncio.base_events
import asyncio.events
import asyncio.log
import heapq
import selectors
import sys
import threading

from android.os import Handler, Looper, MessageQueue
from java import dynamic_proxy
from java.io import FileDescriptor
from java.lang import Runnable

# Some methods in this file are based on CPython's implementation.
# Per https://github.com/python/cpython/blob/master/LICENSE , re-use is permitted
# via the Python Software Foundation License Version 2, which includes inclusion
# into this project under its BSD license terms so long as we retain this copyright notice:
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
# 2014, 2015, 2016, 2017, 2018, 2019, 2020 Python Software Foundation; All Rights Reserved.


class AndroidEventLoop(asyncio.SelectorEventLoop):
    # `AndroidEventLoop` exists to support starting the Python event loop cooperatively with
    # the built-in Android event loop. Since it's cooperative, it has a `run_forever_cooperatively()`
    # method which returns immediately. This is is different from the parent class's `run_forever()`,
    # which blocks.
    #
    # In some cases, for simplicity of implementation, this class reaches into the internals of the
    # parent and grandparent classes.
    #
    # A Python event loop handles two kinds of tasks. It needs to run delayed tasks after waiting
    # the right amount of time, and it needs to do I/O when file descriptors are ready for I/O.
    #
    # `SelectorEventLoop` uses an approach we **cannot** use: it calls the `select()` method
    # to block waiting for specific file descriptors to be come ready for I/O, or a timeout
    # corresponding to the soonest delayed task, whichever occurs sooner.
    #
    # To handle delayed tasks, `AndroidEventLoop` asks the Android event loop to wake it up when
    # its soonest delayed task is ready. To accomplish this, it relies on a `SelectorEventLoop`
    # implementation detail: `_scheduled` is a collection of tasks sorted by soonest wakeup time.
    #
    # To handle waking up when it's possible to do I/O, `AndroidEventLoop` will register file descriptors
    # with the Android event loop so the platform can wake it up accordingly. It does not do this yet.
    def __init__(self):
        # Tell the parent constructor to use our custom Selector.
        selector = AndroidSelector(self)
        super().__init__(selector)
        # Create placeholders for lazily-created objects.
        self.android_interop = AndroidInterop()

    # Override parent `_call_soon()` to ensure Android wakes us up to do the delayed task.
    def _call_soon(self, callback, args, context):
        ret = super()._call_soon(callback, args, context)
        self.enqueue_android_wakeup_for_delayed_tasks()
        return ret

    # Override parent `_add_callback()` to ensure Android wakes us up to do the delayed task.
    def _add_callback(self, handle):
        ret = super()._add_callback(handle)
        self.enqueue_android_wakeup_for_delayed_tasks()
        return ret

    def run_forever_cooperatively(self):
        """Configure the event loop so it is started, doing as little work as possible to
        ensure that. Most Android interop objects are created lazily so that the cost of
        event loop interop is not paid by apps that don't use the event loop."""
        # Based on `BaseEventLoop.run_forever()` in CPython.
        if self.is_running():
            raise RuntimeError(
                "Refusing to start since loop is already running."
            )  # pragma: no cover
        if self._closed:
            raise RuntimeError(
                "Event loop is closed. Create a new object."
            )  # pragma: no cover
        self._set_coroutine_origin_tracking(self._debug)
        self._thread_id = threading.get_ident()

        self._old_agen_hooks = sys.get_asyncgen_hooks()
        sys.set_asyncgen_hooks(
            firstiter=self._asyncgen_firstiter_hook,
            finalizer=self._asyncgen_finalizer_hook,
        )
        asyncio.events._set_running_loop(self)

        # Schedule any tasks which were added before the loop started.
        self.enqueue_android_wakeup_for_delayed_tasks()

    def enqueue_android_wakeup_for_delayed_tasks(self):
        """Ask Android to wake us up when delayed tasks are ready to be handled.

        Since this is effectively the actual event loop, it also handles stopping the
        loop.
        """
        # If we are supposed to stop, actually stop.
        if self._stopping:  # pragma: no cover
            self._stopping = False
            self._thread_id = None
            asyncio.events._set_running_loop(None)
            self._set_coroutine_origin_tracking(False)
            sys.set_asyncgen_hooks(*self._old_agen_hooks)
            # Remove Android event loop interop objects.
            self.android_interop = None
            return

        # If we have actually already stopped, then do nothing.
        if self._thread_id is None:
            return

        timeout = self._get_next_delayed_task_wakeup()
        if timeout is None:
            # No delayed tasks.
            return

        # Ask Android to wake us up to run delayed tasks. Running delayed tasks also
        # checks for other tasks that require wakeup by calling this method. The fact that
        # running delayed tasks can trigger the next wakeup is what makes this event loop a "loop."
        self.android_interop.call_later(self.run_delayed_tasks, timeout * 1000)

    def _set_coroutine_origin_tracking(self, debug):
        # If running on Python 3.7 or 3.8, integrate with upstream event loop's debug feature, allowing
        # unawaited coroutines to have some useful info logged. See https://bugs.python.org/issue32591
        if hasattr(super(), "_set_coroutine_origin_tracking"):  # pragma: no cover
            super()._set_coroutine_origin_tracking(debug)

    def _get_next_delayed_task_wakeup(self):
        """Compute the time to sleep before we should be woken up to handle delayed tasks."""
        # This is based heavily on the CPython's implementation of `BaseEventLoop._run_once()`
        # before it blocks on `select()`.
        _MIN_SCHEDULED_TIMER_HANDLES = 100
        _MIN_CANCELLED_TIMER_HANDLES_FRACTION = 0.5
        MAXIMUM_SELECT_TIMEOUT = 24 * 3600

        sched_count = len(self._scheduled)
        if (
            sched_count > _MIN_SCHEDULED_TIMER_HANDLES
            and self._timer_cancelled_count / sched_count
            > _MIN_CANCELLED_TIMER_HANDLES_FRACTION
        ):  # pragma: no cover
            # Remove delayed calls that were cancelled if their number
            # is too high
            new_scheduled = []
            for handle in self._scheduled:
                if handle._cancelled:
                    handle._scheduled = False
                else:
                    new_scheduled.append(handle)

            heapq.heapify(new_scheduled)
            self._scheduled = new_scheduled
            self._timer_cancelled_count = 0
        else:
            # Remove delayed calls that were cancelled from head of queue.
            while self._scheduled and self._scheduled[0]._cancelled:
                self._timer_cancelled_count -= 1
                handle = heapq.heappop(self._scheduled)
                handle._scheduled = False

        timeout = None
        if self._ready or self._stopping:
            if self._debug:  # pragma: no cover
                print("AndroidEventLoop: self.ready is", self._ready)
            timeout = 0
        elif self._scheduled:
            # Compute the desired timeout.
            when = self._scheduled[0]._when
            timeout = min(max(0, when - self.time()), MAXIMUM_SELECT_TIMEOUT)

        return timeout

    def run_delayed_tasks(self):
        """Android-specific: Run any delayed tasks that have become ready. Additionally,
        check if there are more delayed tasks to execute in the future; if so, schedule
        the next wakeup.
        """
        # Based heavily on `BaseEventLoop._run_once()` from CPython -- specifically, the part
        # after blocking on `select()`.
        # Handle 'later' callbacks that are ready.
        end_time = self.time() + self._clock_resolution
        while self._scheduled:
            handle = self._scheduled[0]
            if handle._when >= end_time:
                break
            handle = heapq.heappop(self._scheduled)
            handle._scheduled = False
            self._ready.append(handle)

        # This is the only place where callbacks are actually *called*.
        # All other places just add them to ready.
        # Note: We run all currently scheduled callbacks, but not any
        # callbacks scheduled by callbacks run this time around --
        # they will be run the next time (after another I/O poll).
        # Use an idiom that is thread-safe without using locks.
        ntodo = len(self._ready)
        for i in range(ntodo):
            handle = self._ready.popleft()
            if handle._cancelled:
                continue  # pragma: no cover
            if self._debug:  # pragma: no cover
                try:
                    self._current_handle = handle
                    t0 = self.time()
                    handle._run()
                    dt = self.time() - t0
                    if dt >= self.slow_callback_duration:
                        asyncio.log.logger.warning(
                            "Executing %s took %.3f seconds",
                            asyncio.base_events._format_handle(handle),
                            dt,
                        )
                finally:
                    self._current_handle = None
            else:
                handle._run()
        handle = None  # Needed to break cycles when an exception occurs.

        # End code borrowed from CPython, within this method.
        self.enqueue_android_wakeup_for_delayed_tasks()


class AndroidInterop:
    """Encapsulate details of Android event loop cooperation."""

    def __init__(self):
        # `_runnable_by_fn` is a one-to-one mapping from Python callables to Java Runnables.
        # This allows us to avoid creating more than one Java object per Python callable, which
        # would prevent removeCallbacks from working.
        self._runnable_by_fn = {}
        # The handler must be created on the Android UI thread.
        self.handler = Handler()

    def get_or_create_runnable(self, fn):
        if fn in self._runnable_by_fn:
            return self._runnable_by_fn[fn]

        self._runnable_by_fn[fn] = PythonRunnable(fn)
        return self._runnable_by_fn[fn]

    def call_later(self, fn, timeout_millis):
        """Enqueue a Python callable `fn` to be run after `timeout_millis` milliseconds."""
        runnable = self.get_or_create_runnable(fn)
        self.handler.removeCallbacks(runnable)
        self.handler.postDelayed(runnable, int(timeout_millis))


class PythonRunnable(dynamic_proxy(Runnable)):
    """Bind a specific Python callable in a Java `Runnable`."""

    def __init__(self, fn):
        super().__init__()
        self._fn = fn

    def run(self):
        self._fn()


class AndroidSelector(selectors.SelectSelector):
    """Subclass of selectors.Selector which cooperates with the Android event loop
    to learn when file descriptors become ready for I/O.

    AndroidSelector's `select()` raises NotImplementedError; see its comments."""

    def __init__(self, loop):
        super().__init__()
        self.loop = loop
        # Lazily-created AndroidSelectorFileDescriptorEventsListener.
        self._file_descriptor_event_listener = None
        # Keep a `_debug` flag so that a developer can modify it for more debug printing.
        self._debug = False

    @property
    def file_descriptor_event_listener(self):
        if self._file_descriptor_event_listener is not None:
            return self._file_descriptor_event_listener
        self._file_descriptor_event_listener = (
            AndroidSelectorFileDescriptorEventsListener(
                android_selector=self,
            )
        )
        return self._file_descriptor_event_listener

    @property
    def message_queue(self):
        return Looper.getMainLooper().getQueue()

    # File descriptors can be registered and unregistered by the event loop.
    # The events for which we listen can be modified. For register & unregister,
    # we mostly rely on the parent class. For modify(), the parent class calls
    # unregister() and register(), so we rely on that as well.

    def register(self, fileobj, events, data=None):
        if self._debug:  # pragma: no cover
            print(
                "register() fileobj={fileobj} events={events} data={data}".format(
                    fileobj=fileobj, events=events, data=data
                )
            )
        ret = super().register(fileobj, events, data=data)
        self.register_with_android(fileobj, events)
        return ret

    def unregister(self, fileobj):  # pragma: no cover
        self.message_queue.removeOnFileDescriptorEventListener(_create_java_fd(fileobj))
        return super().unregister(fileobj)

    def reregister_with_android_soon(self, fileobj):
        def _reregister():
            # If the fileobj got unregistered, exit early.
            key = self._key_from_fd(fileobj)
            if key is None:  # pragma: no cover
                if self._debug:
                    print(
                        "reregister_with_android_soon reregister_temporarily_ignored_fd exiting early; key=None"
                    )
                return
            if self._debug:  # pragma: no cover
                print(
                    "reregister_with_android_soon reregistering key={key}".format(
                        key=key
                    )
                )
            self.register_with_android(key.fd, key.events)

        # Use `call_later(0, fn)` to ensure the Python event loop runs to completion before re-registering.
        self.loop.call_later(0, _reregister)

    def register_with_android(self, fileobj, events):
        if self._debug:  # pragma: no cover
            print(
                "register_with_android() fileobj={fileobj} events={events}".format(
                    fileobj=fileobj, events=events
                )
            )
        # `events` is a bitset comprised of `selectors.EVENT_READ` and `selectors.EVENT_WRITE`.
        # Register this FD for read and/or write events from Android.
        self.message_queue.addOnFileDescriptorEventListener(
            _create_java_fd(fileobj),
            events,  # Passing `events` as-is because Android and Python use the same values for read & write events.
            self.file_descriptor_event_listener,
        )

    def handle_fd_wakeup(self, fd, events):
        """Accept a FD and the events that it is ready for (read and/or write).

        Filter the events to just those that are registered, then notify the loop."""
        key = self._key_from_fd(fd)
        if key is None:  # pragma: no cover
            print(
                "Warning: handle_fd_wakeup: wakeup for unregistered fd={fd}".format(
                    fd=fd
                )
            )
            return

        key_event_pairs = []
        for event_type in (selectors.EVENT_READ, selectors.EVENT_WRITE):
            if events & event_type and key.events & event_type:
                key_event_pairs.append((key, event_type))
        if key_event_pairs:
            if self._debug:  # pragma: no cover
                print(
                    "handle_fd_wakeup() calling parent for key_event_pairs={key_event_pairs}".format(
                        key_event_pairs=key_event_pairs
                    )
                )
            # Call superclass private method to notify.
            self.loop._process_events(key_event_pairs)
        else:  # pragma: no cover
            print(
                "Warning: handle_fd_wakeup(): unnecessary wakeup fd={fd} events={events} key={key}".format(
                    fd=fd, events=events, key=key
                )
            )

    # This class declines to implement the `select()` method, purely as
    # a safety mechanism. On Android, this would be an error -- it would result
    # in the app freezing, triggering an App Not Responding pop-up from the
    # platform, and the user killing the app.
    #
    # Instead, the AndroidEventLoop cooperates with the native Android event
    # loop to be woken up to get work done as needed.
    def select(self, *args, **kwargs):
        raise NotImplementedError("AndroidSelector refuses to select(); see comments.")


class AndroidSelectorFileDescriptorEventsListener(
    dynamic_proxy(MessageQueue.OnFileDescriptorEventListener)
):
    """Notify an `AndroidSelector` instance when file descriptors become readable/writable."""

    def __init__(self, android_selector):
        super().__init__()
        self.android_selector = android_selector
        # Keep a `_debug` flag so that a developer can modify it for more debug printing.
        self._debug = False

    def onFileDescriptorEvents(self, fd_obj, events):
        """Receive a Java FileDescriptor object and notify the Python event loop that the FD
        is ready for read and/or write.

        As an implementation detail, this relies on the fact that Android EVENT_INPUT and Python
        selectors.EVENT_READ have the same value (1) and Android EVENT_OUTPUT and Python
        selectors.EVENT_WRITE have the same value (2)."""
        # Call hidden (non-private) method to get the numeric FD, so we can pass that to Python.
        fd = getattr(fd_obj, "getInt$")()
        if self._debug:  # pragma: no cover
            print(
                "onFileDescriptorEvents woke up for fd={fd} events={events}".format(
                    fd=fd, events=events
                )
            )
        # Tell the Python event loop that the FD is ready for read and/or write.
        self.android_selector.handle_fd_wakeup(fd, events)
        # Tell Android we don't want any more wake-ups from this FD until the event loop runs.
        # To do that, we return 0.
        #
        # We also need Python to request wake-ups once the event loop has finished.
        self.android_selector.reregister_with_android_soon(fd)
        return 0


def _create_java_fd(int_fd):
    """Given a numeric file descriptor, create a `java.io.FileDescriptor` object."""
    # On Android, the class exposes hidden (non-private) methods `getInt$()` and `setInt$()`. Because
    # they aren't valid Python identifier names, we need to use `getattr()` to grab them.
    # See e.g. https://android.googlesource.com/platform/prebuilts/fullsdk/sources/android-28/+/refs/heads/master/java/io/FileDescriptor.java#149 # noqa: E501
    java_fd = FileDescriptor()
    getattr(java_fd, "setInt$")(int_fd)
    return java_fd
