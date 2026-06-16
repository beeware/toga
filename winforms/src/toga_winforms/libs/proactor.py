import _overlapped
import _winapi
import asyncio
import sys
import threading
import time
import traceback
from asyncio import events
from asyncio.log import logger
from asyncio.windows_events import _WaitCancelFuture
from collections import deque

import System.Windows.Forms as WinForms
from System import Action
from System.Threading.Tasks import Task

from toga.handlers import WeakrefCallable


class ReadyDeque(deque):
    """A deque that enqueues a WinForms event tick when a value is appended."""

    def __init__(self, loop):
        super().__init__(loop._ready)
        self._loop = loop
        self._enqueue_tick = loop.enqueue_tick

    def append(self, value):
        super().append(value)
        if getattr(getattr(self, "_loop", None), "_idle", False):
            self._enqueue_tick(delay=0)


class TwoThreadIocpProactor(asyncio.IocpProactor):
    """A version of the IocpProactor class where the IOCP will run on its own thread."""

    ####################################################################################
    # Overrides of asyncio.IocpProactor methods
    ####################################################################################

    def __init__(self, concurrency=_winapi.INFINITE):
        super().__init__(concurrency)
        self._cache_cleanup_complete = False

        self._listener_lock = threading.Lock()
        self._cleanup_lock = threading.Lock()
        self._exit_lock = threading.Lock()

        self._cleanup_lock.acquire()

    def select(self, timeout=None):
        """A blank select method so that _run_once doesn't poll the IOCP."""
        return []

    # This method is part of the app shutdown procedure, which can't have test coverage.
    # So this method is marked as no cover.
    def close(self):  # pragma: no cover
        if self._iocp is None:
            # Already closed.
            return

        # Wait until the IOCP listener has stopped before cleaning up the cache.
        with self._listener_lock:
            self._remove_unregistered_futures()

        # The following codeblock is from the start of the asyncio.IocpProactor.close()
        # method. The final part of the this method is in the _iocp_listener_cleanup()
        # method. The reason for splitting the close method is because the polling
        # function GetQueuedCompletionStatus becomes associated to the first thread that
        # calls it and it can be associated to at most one thread. See:
        # learn.microsoft.com/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatus # noqa E501
        #
        # fmt: off
        # ruff: disable[B007]
        # =================================== BEGIN ===================================
        # Cancel remaining registered operations.
        for fut, ov, obj, callback in list(self._cache.values()):
            if fut.cancelled():
                # Nothing to do with cancelled futures
                pass
            elif isinstance(fut, _WaitCancelFuture):
                # _WaitCancelFuture must not be cancelled
                pass
            else:
                try:
                    fut.cancel()
                except OSError as exc:
                    if self._loop is not None:
                        context = {
                            'message': 'Cancelling a future failed',
                            'exception': exc,
                            'future': fut,
                        }
                        if fut._source_traceback:
                            context['source_traceback'] = fut._source_traceback
                        self._loop.call_exception_handler(context)
        # ==================================== END ====================================
        # ruff: enable[B007]
        # fmt: on

        # Let the ICOP thread receive the final messages.
        self._cleanup_lock.release()

        # Wait for the ICOP thread to shutdown before continuing.
        with self._exit_lock:
            _winapi.CloseHandle(self._iocp)
            self._iocp = None

    ####################################################################################
    # Methods that run in the IOCP listener thread.
    ####################################################################################

    def _iocp_listener(self):
        """Listens for IOCP events and adds them to the queue."""
        # The exit lock prevents the TwoThreadIocpProactor loop from closing before
        # the IOCP listener thread has shutdown correctly.
        with self._exit_lock:
            # The listener lock forces the close method to wait until the listener
            # loop is closed.
            with self._listener_lock:
                app = self._loop.app
                app_dispatcher = self._loop.app.app_dispatcher
                GetQueuedCompletionStatus = _overlapped.GetQueuedCompletionStatus

                while not app._is_exiting:
                    # Use a timeout (100 milliseconds) only for exiting the thread.
                    status = GetQueuedCompletionStatus(self._iocp, 100)

                    if status is None:

                        def iocp_action():
                            return self._remove_unregistered_futures()

                    else:

                        def iocp_action(status=status):
                            return self._iocp_action(status)

                    # Inkove the actions synchronously on the main thread.
                    app_dispatcher.Invoke(Action(iocp_action))

                ########################################################################
                # From here onward is part of the app shutdown procedure, which can't
                # have test coverage. So use no cover.
                ########################################################################

                # Exit the application. Call here to avoid dispatcher calls after
                # app.native is exited.
                action = Action(lambda: app.native.Exit())  # pragma: no cover
                app_dispatcher.Invoke(action)  # pragma: no cover

            # Wait until the close method has cleaned up the cache before continuing.
            with self._cleanup_lock:  # pragma: no cover
                self._iocp_listener_cleanup()  # pragma: no cover

    # This method is part of the app shutdown procedure, which can't have test coverage.
    # So this method is marked as no cover.
    def _iocp_listener_cleanup(self):  # pragma: no cover
        """Cleanup the IOCP listener thread before exiting."""
        # The following is the last 19 lines of code from asyncio.IocpProactor.close
        # method. All the first line of this method remain in the close method.
        #
        # fmt: off
        # =================================== BEGIN ===================================
        # Wait until all cancelled overlapped complete: don't exit with running
        # overlapped to prevent a crash. Display progress every second if the
        # loop is still running.
        msg_update = 1.0
        start_time = time.monotonic()
        next_msg = start_time + msg_update
        while self._cache:
            if next_msg <= time.monotonic():
                logger.debug('%r is running after closing for %.1f seconds',
                             self, time.monotonic() - start_time)
                next_msg = time.monotonic() + msg_update

            # handle a few events, or timeout
            self._poll(msg_update)

        self._results = []
        # ==================================== END ====================================
        # fmt: on

    ####################################################################################
    # Methods that run in the main application thread.
    ####################################################################################

    def start_iocp_listener(self):
        self._iocp_thread = threading.Thread(
            target=self._run_iocp_listener,
        )
        self._iocp_thread.start()

    def _run_iocp_listener(self):
        self._iocp_listener()

    def _iocp_action(self, status):
        # The following codeblock is essentially the same as part of the method
        # asyncio.IocpProactor._poll(timeout). Here the futures are no longer appended
        # to the self._results list, since this served no purpose in the proactor event
        # loop. This codeblock is part of the method that processes the received IOCP
        # messages.
        #
        # fmt: off
        # ruff: disable[UP031]
        # =================================== BEGIN ===================================
        err, transferred, key, address = status
        try:
            f, ov, obj, callback = self._cache.pop(address)
        except KeyError:
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

        if obj in self._stopped_serving:
            f.cancel()
        # Don't call the callback if _register() already read the result or
        # if the overlapped has been cancelled
        elif not f.done():
            try:
                value = callback(transferred, key, ov)
            except OSError as e:
                f.set_exception(e)
                # self._results.append(f)
            else:
                f.set_result(value)
                # self._results.append(f)
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
        self._idle = True

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
        # Python 3.8 added an implementation of run_forever() in
        # ProactorEventLoop. The only part that actually matters is the
        # refactoring that moved the initial call to stage _loop_self_reading;
        # it now needs to be created as part of run_forever; otherwise the
        # event loop locks up, because there won't be anything for the
        # select call to process.
        self.call_soon(self._loop_self_reading)

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

        # Rather than going into a `while True:` loop, we're going to use the
        # Winforms event loop to queue a tick() message that will cause a
        # single iteration of the asyncio event loop to be executed. Each time
        # we do this, we queue *another* tick() message in 5ms time. In this
        # way, we'll get a continuous stream of tick() calls, without blocking
        # the Winforms event loop. We also add a handler for ApplicationExit
        # to ensure that loop cleanup occurs when the app exits.

        WinForms.Application.ApplicationExit += WeakrefCallable(
            self.winforms_application_exit
        )

        # Queue the first asyncio tick.
        self.enqueue_tick()

        # Change the ready deque to an instance of ReadyDeque.
        self._ready = ReadyDeque(self)

        # Start the IOCP listener thread.
        self._proactor.start_iocp_listener()

        # Start the Winforms event loop.
        self._inner_loop = None
        WinForms.Application.Run(self.app.app_context)

    def enqueue_tick(self, delay=5):
        # Queue a call to tick in a specified delay.
        self.task = Action[Task](self.tick)
        Task.Delay(delay).ContinueWith(self.task)

    # This function doesn't report as covered because it runs on a
    # non-Python-created thread (see App.run_app). But it must actually be
    # covered, otherwise nothing would work.
    def tick(self, *args, **kwargs):  # pragma: no cover
        """Cause a single iteration of the event loop to run on the main GUI thread."""
        action = Action(self.run_once_recurring)
        self.app.app_dispatcher.Invoke(action)

    # The native dialog `Show` methods are all blocking, as they run an inner native
    # event loop. Call them via this method to ensure the inner loop is correctly linked
    # with this Python loop.
    def start_inner_loop(self, callback, *args):
        assert self._inner_loop is None
        self._inner_loop = (callback, args)
        self.enqueue_tick(delay=0)

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

    def run_once_recurring(self):
        """Run one iteration of the event loop, and enqueue the next iteration (if we're
        not stopping).
        """
        # run_once_recurring is called asynchronously by the native WinForms loop. The
        # tasks that triggered the call may have already been processed.
        if len(self._ready) < 1 and len(self._scheduled) < 1 and not self._inner_loop:
            return

        try:
            # If the app is exiting, stop the asyncio event loop.
            # Otherwise, perform one more tick of the event loop.
            # We can't get coverage of app shutdown, so that branch
            # is marked no cover
            if self.app._is_exiting:
                self.stop()  # pragma: no cover
            else:
                if len(self._ready) > 0 or len(self._scheduled) > 0:
                    self._idle = False
                    self._run_once()
                    self._idle = True

            # Enqueue the next tick. Determine the delay of the tick by checking if
            # there are events in the ready list, otherwise then calculating a delay
            # for scheduled events. If neither of these then the loop becomes idle
            # until it is woken by the ReadyDeque instance.
            if len(self._ready) > 0:
                # Run ready events immiediately.
                self.enqueue_tick(delay=0)
            else:
                if self._scheduled:
                    # Calculate a delay for scheduled events and enqueue a tick.
                    first = self._scheduled[0]
                    ms_until = int(max(0, (first.when() - self.time()) * 1000))
                    delay = min(1000, ms_until)
                    self.enqueue_tick(delay=delay)

            if self._inner_loop:
                callback, args = self._inner_loop
                self._inner_loop = None
                callback(*args)

        # Exceptions thrown by this method will be silently ignored.
        except BaseException:  # pragma: no cover
            traceback.print_exc()
