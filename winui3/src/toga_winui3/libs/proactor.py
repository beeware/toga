import _overlapped
import _winapi
import asyncio
import sys
import threading
import traceback
from asyncio import events
from collections import deque
from ctypes import byref

from win32more import UInt64
from win32more.Microsoft.UI.Dispatching import DispatcherQueue
from win32more.Windows.Foundation import TimeSpan
from win32more.Windows.Win32.System.WindowsProgramming import QueryInterruptTimePrecise


class ReadyDeque(deque):
    """A deque that enqueues a WinUI3 event tick when a value is appended."""

    def __init__(self, loop):
        self._loop = loop
        super().__init__(loop._ready)

    def append(self, value):
        super().append(value)

        if self._loop._idle:
            self._loop.enqueue_tick(delay=0)


class TwoThreadIocpProactor(asyncio.IocpProactor):
    """A version of the IocpProactor class where the IOCP will run on its own thread."""

    ####################################################################################
    # Overrides of asyncio.IocpProactor methods
    ####################################################################################

    def __init__(self):
        super().__init__()
        self._listener_lock = threading.Lock()

    def select(self, timeout=None):
        """A minimal select method so that _run_once doesn't poll the IOCP."""
        # Clear the results of the processed IOCP messages.
        self._results = []
        return []

    # This method is part of the app shutdown procedure, which can't have test coverage.
    # So this method is marked as no cover.
    def close(self):  # pragma: no cover
        if self._iocp is None:
            # Already closed.
            return

        # The loop needs the app to run and visa versa. So ensure that the app is exited
        # if `close()` is called.
        self._loop.app._is_exiting = True

        # Wait until the IOCP listener has stopped before closing the loop.
        with self._listener_lock:
            self._remove_unregistered_futures()

        super().close()

    ####################################################################################
    # Methods that run in the IOCP listener thread.
    ####################################################################################

    def _iocp_listener(self):
        """Listens for IOCP events and adds them to the queue."""
        app = self._loop.app
        task_enqueuer = self._loop.task_enqueuer
        GetQueuedCompletionStatus = _overlapped.GetQueuedCompletionStatus

        # The listener lock forces the close method to wait until the listener
        # loop is closed.
        with self._listener_lock:
            while not app._is_exiting:
                # Use a timeout (100 milliseconds) only for exiting the thread.
                status = GetQueuedCompletionStatus(self._iocp, 100)

                if status is None:

                    def iocp_action():
                        return self._remove_unregistered_futures()

                else:

                    def iocp_action(status=status):
                        return self._iocp_action(status)

                # Queue/run the actions to run synchronously on the main thread.
                task_enqueuer(iocp_action)

            ############################################################################
            # From here onward is part of the app shutdown procedure, which can't have
            # test coverage. So use no cover.
            ############################################################################

            # Exit the application. Call here to avoid dispatcher calls after
            # app.native is exited.

            def exit_native():  # pragma: no cover
                # Make sure that the Win32-based StatusIcons are closed correctly.
                for status_icon in app.interface.status_icons:
                    status_icon._impl.remove()

                app.native.Exit(app.native_instance)

            task_enqueuer(exit_native)  # pragma: no cover

    ####################################################################################
    # Methods that run in the main application thread.
    ####################################################################################

    def start_iocp_listener(self):
        self._iocp_thread = threading.Thread(
            target=self._iocp_listener,
        )
        self._iocp_thread.start()

    def _iocp_action(self, status):
        # The following codeblock is the part of asyncio.IocpProactor._poll(timeout)
        # that processes the received IOCP messages.
        #
        # Use no cover for the KeyError and OSError codeblocks since these should not be
        # accessed under normal operations.
        #
        # Use no cover obj in self._stopped_serving since this list is only populated
        # by the self._stop_serving method, which is only called in the loop.close
        # method. The loop.close method is part of the shutdown procedure, so no cover.
        #
        # Use no branch for f.done() since it is not consistently hit during normal
        # operations.
        #
        # fmt: off
        # ruff: disable[UP031]
        # =================================== BEGIN ===================================
        err, transferred, key, address = status
        try:
            f, ov, obj, callback = self._cache.pop(address)
        except KeyError: # pragma: no cover
            if self._loop.get_debug():
                self._loop.call_exception_handler({
                    'message': ('GetQueuedCompletionStatus() returned an '
                                'unexpected event'),
                    'status': ('err=%s transferred=%s key=%#x address=%#x'
                                % (err, transferred, key, address)),
                })

            # key is either zero, or it is used to return a pipe
            # handle which should be closed to avoid a leak.
            if key not in (0, _overlapped.INVALID_HANDLE_VALUE):
                _winapi.CloseHandle(key)
            return

        if obj in self._stopped_serving: # pragma: no cover
            f.cancel()
        # Don't call the callback if _register() already read the result or
        # if the overlapped has been cancelled
        elif not f.done(): # pragma: no branch
            try:
                value = callback(transferred, key, ov)
            except OSError as e: # pragma: no cover
                f.set_exception(e)
                self._results.append(f)
            else:
                f.set_result(value)
                self._results.append(f)
            finally:
                f = None
        # ==================================== END ====================================
        # ruff: enable[UP031]
        # fmt: on

    def _remove_unregistered_futures(self):
        # Remove unregistered futures
        for ov in self._unregistered:
            self._cache.pop(ov.address, None)
        self._unregistered.clear()


class WinUI3ProactorEventLoop(asyncio.ProactorEventLoop):
    def __init__(self):
        super().__init__(proactor=TwoThreadIocpProactor())
        self._idle = True

    def run_forever(self, app):
        """Set up the asyncio event loop, integrate it with the native event loop, and
        start the application.

        This largely duplicates the setup behavior of the default Proactor
        run_forever implementation.

        :param app_context: The WinForms.ApplicationContext instance
            controlling the lifecycle of the app.
        """
        # Remember the application.
        self.app = app

        # Set up the Proactor.
        if sys.version_info < (3, 13):
            # The code between the following markers should be exactly the same
            # as the official CPython implementation, up to the start of the
            # `while True:` part of run_forever() (see
            # BaseEventLoop.run_forever() in Lib/ascynio/base_events.py). In
            # Python 3.13.0a2, this was refactored into the
            # `_run_forever_setup()` helper. We run testbed on Py3.10, so the
            # else branch is marked nocover.
            # === START BaseEventLoop.run_forever() setup ===
            self._check_closed()
            if self.is_running():  # pragma: no cover
                raise RuntimeError("This event loop is already running")
            if events._get_running_loop() is not None:  # pragma: no cover
                raise RuntimeError(
                    "Cannot run the event loop while another loop is running"
                )
            self._thread_id = threading.get_ident()
            self._old_agen_hooks = sys.get_asyncgen_hooks()
            sys.set_asyncgen_hooks(
                firstiter=self._asyncgen_firstiter_hook,
                finalizer=self._asyncgen_finalizer_hook,
            )

            events._set_running_loop(self)
            # === END BaseEventLoop.run_forever() setup ===
        else:  # pragma: no cover
            self._orig_state = self._run_forever_setup()

        # Change the ready deque to an instance of ReadyDeque.
        self._ready = ReadyDeque(self)

        def on_lauched(winui3_app, args):
            return self.native_app_launched(winui3_app, args)

        app.native.OnLaunched = on_lauched

        # Start the native event loop.
        app.native.Start()

    def time(self):
        """A timer that is accurate to 100 nanoseconds.

        The standard asyncio time method uses the CPython time.monotonic function
        which obtains the time from GetProcessTimes. This has a resolution of 15.6 ms,
        which comes from the default Windows system timer.
        """
        precise_time = UInt64()
        QueryInterruptTimePrecise(byref(precise_time))
        return precise_time.value / 10000000

    # Can't get coverage for app shutdown, so this handler must be no-cover.
    def app_exiting(loop, winui3_app):  # pragma: no cover
        """Perform cleanup that needs to occur when the app exits.

        This largely duplicates the "finally" behavior of the default Proactor
        run_forever implementation.
        """
        if sys.version_info < (3, 13):
            # If we're stopping, we can do the "finally" handling from
            # the BaseEventLoop run_forever(). In Python 3.13.0a2, this
            # was refactored into the `_run_forever_cleanup()` helper.
            # We run testbed on Py3.12, so the else branch is marked
            # nocover.
            # === START BaseEventLoop.run_forever() finally handling ===
            loop._stopping = False
            loop._thread_id = None
            events._set_running_loop(None)
            loop._set_coroutine_origin_tracking(False)
            sys.set_asyncgen_hooks(*loop._old_agen_hooks)
            # === END BaseEventLoop.run_forever() finally handling ===
        else:  # pragma: no cover
            loop._run_forever_cleanup()

    def native_app_launched(self, winui3_app, args):
        """A function to be used as an override of the OnLauched method of NativeApp."""
        dispatcher = DispatcherQueue.GetForCurrentThread()
        self.task_enqueuer = dispatcher.TryEnqueue

        self.tick_scheduler = dispatcher.CreateTimer()
        self.tick_scheduler.IsRepeating = False
        self.tick_scheduler.Tick += self.tick

        # Start the IOCP listener thread.
        self._proactor.start_iocp_listener()

        self.app.native_instance = winui3_app
        asyncio.set_event_loop(self)
        self.enqueue_tick()

    def enqueue_tick(self, delay=5):
        # Queue a call to tick in a specified delay.
        # delay is given in 100-nanosecond units i.e. 1E-7 seconds.
        self.tick_scheduler.Interval = TimeSpan(delay)
        self.tick_scheduler.Start()

    def tick(self, *args, **kwargs):  # pragma: no cover
        """Cause a single iteration of the event loop to run on the main GUI thread."""
        # FIXME: For some reason the queue timer doesn't work properly when the
        # following line is removed.
        self.tick_scheduler.IsRunning  # noqa: B018
        self.run_once_recurring()

    def run_once_recurring(self):
        """Run one iteration of the event loop, and enqueue the next iteration (if we're
        not stopping).
        """
        # run_once_recurring is called asynchronously by the native WinForms loop. The
        # tasks that triggered the call may have already been processed.
        if len(self._ready) < 1 and len(self._scheduled) < 1:
            return

        try:
            # If the app is exiting, stop the asyncio event loop.
            # Otherwise, perform one more tick of the event loop.
            # We can't get coverage of app shutdown, so that branch
            # is marked no cover
            if self.app._is_exiting:
                self.stop()  # pragma: no cover
            else:
                self._idle = False
                self._run_once()
                self._idle = True

            # Enqueue the next tick. Determine the delay of the tick by checking if
            # there are events in the ready list, otherwise then calculating a delay
            # for scheduled events. If neither of these then the loop becomes idle
            # until it is woken by the ReadyDeque instance or the safety catch.
            if len(self._ready) > 0:
                # Run ready events immediately.
                self.enqueue_tick(delay=0)
            else:
                if self._scheduled:
                    # Calculate a delay for scheduled events and enqueue a tick.
                    first = self._scheduled[0]
                    delay = int(max(0, (first.when() - self.time()) * 10000000))
                    self.enqueue_tick(delay=delay)

        # Exceptions thrown by this method will be silently ignored.
        except BaseException:  # pragma: no cover
            traceback.print_exc()
