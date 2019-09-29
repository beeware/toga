import asyncio
import sys
import threading
from asyncio import events

from .winforms import Action, Task


class WinformsProactorEventLoop(asyncio.ProactorEventLoop):
    def setup_run_forever(self, app_context):
        """Set up the asyncio event loop.

        This largely duplicates the setup behavior of the default Proactor
        run_forever implementation.
        """
        self.app_context = app_context

        self._check_closed()
        if self.is_running():
            raise RuntimeError('This event loop is already running')
        if events._get_running_loop() is not None:
            raise RuntimeError(
                'Cannot run the event loop while another loop is running')
        self._set_coroutine_origin_tracking(self._debug)
        self._thread_id = threading.get_ident()
        try:
            self._old_agen_hooks = sys.get_asyncgen_hooks()
            sys.set_asyncgen_hooks(
                firstiter=self._asyncgen_firstiter_hook,
                finalizer=self._asyncgen_finalizer_hook
            )
        except AttributeError:
            # Python < 3.6 didn't have sys.get_asyncgen_hooks();
            # No action required for those versions.
            pass

        events._set_running_loop(self)
        # Queue the first asyncio tick.
        self.queue_tick()

    def queue_tick(self):
        Task.Delay(500).ContinueWith(Action[Task](self.tick))

    def tick(self, *args, **kwargs):
        """
        Run a single iteration of the event loop on the main GUI thread,
        and enqueue the next iteration (if we're not stopping).

        This largely duplicates the "finally" behavior of the default Proactor
        run_forever implementation.
        """
        # Run one iteration of the event loop on the main GUI thread
        if self.app_context.MainForm:
            self.app_context.MainForm.Invoke(Action(self._run_once))

        if self._stopping:
            # If we're stopping, close down the event loop
            self._stopping = False
            self._thread_id = None
            events._set_running_loop(None)
            self._set_coroutine_origin_tracking(False)
            try:
                sys.set_asyncgen_hooks(*self._old_agen_hooks)
            except AttributeError:
                # Python < 3.6 didn't have set_asyncgen_hooks.
                # No action required for those versions.
                pass
        else:
            # Live to tick another day. Enqueue the next tick,
            # and make sure there will be *something* to be processed.
            self.queue_tick()
            self.call_soon_threadsafe(lambda: True)


# Python 3.7 changed the name of an internal wrapper function.
# Install an alias for the old name at the new name.
if sys.version_info < (3, 7):
    WinformsProactorEventLoop._set_coroutine_origin_tracking = WinformsProactorEventLoop._set_coroutine_wrapper
