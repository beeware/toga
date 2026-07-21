import _overlapped
import _winapi
import asyncio
import sys
import threading
import traceback
from asyncio import events
from collections import deque

import System.Windows.Forms as WinForms
from System import Action
from System.Threading.Tasks import Task

from toga.handlers import WeakrefCallable

from .reentrantqueue import ReentrantQueue


class ReadyDeque(deque):
    """A deque that enqueues a WinForms event tick when a value is appended."""

    def __init__(self, loop):
        self._loop = loop
        super().__init__(loop._ready)

    def append(self, value):
        super().append(value)

        if self._loop._idle:
            self._loop.enqueue_task(delay=0, task=self._loop.run_once_recurring)


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
        app_dispatcher = self._loop.app.app_dispatcher
        GetQueuedCompletionStatus = _overlapped.GetQueuedCompletionStatus

        def enqueue_task(task):
            def action():
                return self._loop._synchronous_queue.append(task)

            app_dispatcher.Invoke(Action(action))

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
                enqueue_task(iocp_action)

            ########################################################################
            # From here onward is part of the app shutdown procedure, which can't
            # have test coverage. So use no cover.
            ########################################################################

            # Exit the application. Call here to avoid dispatcher calls after
            # app.native is exited.
            action = Action(lambda: app.native.Exit())  # pragma: no cover
            app_dispatcher.Invoke(action)  # pragma: no cover

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


class WinformsProactorEventLoop(asyncio.ProactorEventLoop):
    def __init__(self):
        super().__init__(proactor=TwoThreadIocpProactor())

        self._synchronous_queue = ReentrantQueue()
        self._idle = True
        self._wake_times = {}

    def run_forever(self, app):
        """Set up the asyncio event loop, integrate it with the Winforms event loop, and
        start the application.

        This largely duplicates the setup behavior of the run_forever implementation of
        asyncio.ProactorEventLoop with two main differences:
            - The need for polling has been removed by running the IOCP on a separate
              thread and using the WinForms event loop to send the results immediately
              to the main thread.
            - The loop on the main thread can become idle when there are no ready or
              scheduled tasks. The self._ready deque has been replaced by an instance
              of ReadyDeque which fires and wakes the loop.

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

        # Rather than using a `while True:` loop, the `run_forever` method piggybacks
        # onto the Winforms event loop:
        # - Ready tasks are enqueued into the WinForms event loop by a ReadyDeque object
        #   using the `enqueue_task` method.
        # - Cleanup is ensured by handling the ApplicationExit event when the app exits.
        # - Completed I/O tasks are enqueued on a separate thread which is started by
        #   the `start_iocp_listener` method.

        WinForms.Application.ApplicationExit += WeakrefCallable(
            self.winforms_application_exit
        )

        # Queue the first asyncio tick.
        self.enqueue_task(delay=0, task=self._safety_catch_task)

        # Change the ready deque to an instance of ReadyDeque.
        self._ready = ReadyDeque(self)

        # Start the IOCP listener thread.
        self._proactor.start_iocp_listener()

        # Start the Winforms event loop.
        self._inner_loop = None
        WinForms.Application.Run(self.app.app_context)

    def enqueue_task(self, task, delay):
        """Use the WinForms event loop to enqueue a task after a given delay."""

        def dispatch_task(*args, task=task, **kwargs):
            return self.dispatch_task(*args, task=task, **kwargs)

        # Add a call which dispactes the Queue a call to tick in a specified delay.
        Task.Delay(delay).ContinueWith(Action[Task](dispatch_task))

    # This function doesn't report as covered because it runs on a
    # non-Python-created thread (see App.run_app). But it must actually be
    # covered, otherwise nothing would work.
    def dispatch_task(self, *args, task=None, **kwargs):  # pragma: no cover
        """Use the WinForms dispatcher to add a given task to the synchronous queue."""

        def enqueue_task_sync(task=task):
            return self._synchronous_queue.append(task)

        # Using the dispatcher ensures that the task is run on the GUI thread.
        self.app.app_dispatcher.Invoke(Action(enqueue_task_sync))

    # The native dialog `Show` methods are all blocking, as they run an inner native
    # event loop. Call them via this method to ensure the inner loop is correctly linked
    # with this Python loop.
    def start_inner_loop(self, callback, *args):
        action = Action(lambda: callback(*args))
        self.app.app_dispatcher.InvokeAsync(action)

    # We can't get coverage for app shutdown, so this handler must be no-cover.
    def winforms_application_exit(self, app, event):  # pragma: no cover
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
            self._stopping = False
            self._thread_id = None
            events._set_running_loop(None)
            self._set_coroutine_origin_tracking(False)
            sys.set_asyncgen_hooks(*self._old_agen_hooks)
            # === END BaseEventLoop.run_forever() finally handling ===
        else:  # pragma: no cover
            self._run_forever_cleanup()

    def run_once_recurring(self, wake_time=None):
        """Run one iteration of the event loop, and (if needed) enqueue the next.

        :param wake_time: A call with `wake_time != None` indicates that the loop has
            been woken in an attempt to run a task at the time given by `wake_time`.
            Note that because of the resolution of the internal clocks, it is possible
            that multiple iterations of the loop will run in an attempt to hit (or pass)
            the time given by `wake_time`.
        """
        # run_once_recurring is called asynchronously by the native WinForms loop. The
        # tasks that triggered the call may have already been processed.
        if len(self._ready) < 1 and len(self._scheduled) < 1:
            return

        try:
            # If the app is exiting, stop the asyncio event loop. Otherwise, perform one
            # more tick of the event loop. We can't get coverage of app shutdown, so
            # that branch is marked no cover.
            if self.app._is_exiting:
                self.stop()  # pragma: no cover
            else:
                self._idle = False
                self._run_once()
                self._idle = True

            # self._wake_times records the target wake times for scheduled events. Get
            # the time for the next scheduled wake-up, and remove and remove any wake
            # times which have passed.
            next_wake = self._scheduled[0].when() if self._scheduled else None
            if next_wake:
                self._wake_times = {t for t in self._wake_times if t >= next_wake}

            # Determine if the loop should become idle, or if another iteration should
            # be enqueued and when. If there is no event to enqueue the loop becomes
            # idle until it is woken by the ReadyDeque instance or the safety catch.
            #
            # Note that for any given `wake_time`, there is only one chain of wake-up
            # calls. This is to prevent the loop constantly rescheduling wake-ups for
            # the same task.
            if len(self._ready) > 0:
                delay = 0

                # If the first scheduled task has the same value as `wake_time` it means
                # that `run_once_recurring` was triggered in an attempt to hit the wake
                # time. It also means that the task has not been processed, so another
                # attempt to hit the scheduled time is needed. So, only change the value
                # of `wake_time` if `next_wake` does not equal `wake_time``.
                if next_wake != wake_time:
                    wake_time = None

            # A wake-up of the loop is scheduled for when the:
            # - First scheduled task is new i.e. `next_wake not in self._wake_times`.
            # - Current loop iteration is an attempt to hit `wake_time` but the first
            #   scheduled task has not been processed i.e. `next_wake == wake_time`.
            elif next_wake and (
                next_wake not in self._wake_times or next_wake == wake_time
            ):
                self._wake_times.add(next_wake)
                delay = int(max(0, (next_wake - self.time()) * 1000))
                wake_time = next_wake

            # If there are no tasks to process or new wake-ups scheduled, the loop
            # becomes idle.
            else:
                return

            def task(wake_time=wake_time):
                self.run_once_recurring(wake_time=wake_time)

            self.enqueue_task(task=task, delay=delay)

        # Exceptions thrown by this method will be silently ignored.
        except BaseException:  # pragma: no cover
            traceback.print_exc()

    ####################################################################################
    # Safety catch - A tick at least every 1 second. This shouldn't be required, but it
    # guarantees that the event loop can't completely stall.
    ####################################################################################

    def _safety_catch_task(self):
        self.enqueue_task(delay=1000, task=self._safety_catch_task)
        self.run_once_recurring()
