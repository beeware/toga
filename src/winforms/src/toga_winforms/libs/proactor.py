import asyncio
import sys
import threading
from asyncio import events

from .winforms import Action, Task, WinForms


class WinformsProactorEventLoop(asyncio.ProactorEventLoop):
    def run_forever(self, app_context):
        """Set up the asyncio event loop, integrate it with the Winforms
        event loop, and start the application.

        This largely duplicates the setup behavior of the default Proactor
        run_forever implementation.

        :param app_context: The WinForms.ApplicationContext instance
            controlling the lifecycle of the app.
        """
        # Python 3.8 added an implementation of run_forever() in
        # ProactorEventLoop. The only part that actually matters is the
        # refactoring that moved the initial call to stage _loop_self_reading;
        # it now needs to be created as part of run_forever; otherwise the
        # event loop locks up, because there won't be anything for the
        # select call to process.
        if sys.version_info >= (3, 8):
            self.call_soon(self._loop_self_reading)

        # Remember the application context.
        self.app_context = app_context

        # Setup the Proactor.
        # The code between the following markers should be exactly the same as
        # the official CPython implementation, up to the start of the
        # `while True:` part of run_forever() (see BaseEventLoop.run_forever()
        # in Lib/ascynio/base_events.py)
        # === START BaseEventLoop.run_forever() setup ===
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
        # === END BaseEventLoop.run_forever() setup ===

        # Rather than going into a `while True:` loop, we're going to use the
        # Winforms event loop to queue a tick() message that will cause a
        # single iteration of the asyncio event loop to be executed. Each time
        # we do this, we queue *another* tick() message in 5ms time. In this
        # way, we'll get a continuous stream of tick() calls, without blocking
        # the Winforms event loop.

        # Queue the first asyncio tick.
        self.enqueue_tick()

        # Start the Winforms event loop.
        WinForms.Application.Run(self.app_context)

    def enqueue_tick(self):
        # Queue a call to tick in 5ms.
        self.task = Action[Task](self.tick)
        Task.Delay(5).ContinueWith(self.task)

    def tick(self, *args, **kwargs):
        """
        Cause a single iteration of the event loop to run on the main GUI thread.
        """
        # FIXME: this only works if there is a "main window" registered with the
        # app (#750).
        #
        # If the app context has a main form, invoke run_once_recurring()
        # on the thread associated with that form.
        if self.app_context.MainForm:
            action = Action(self.run_once_recurring)
            self.app_context.MainForm.Invoke(action)

    def run_once_recurring(self):
        """
        Run one iteration of the event loop, and enqueue the next iteration
        (if we're not stopping).

        This largely duplicates the "finally" behavior of the default Proactor
        run_forever implementation.
        """
        # Perform one tick of the event loop.
        self._run_once()

        if self._stopping:
            # If we're stopping, we can do the "finally" handling from
            # the BaseEventLoop run_forever().
            # === START BaseEventLoop.run_forever() finally handling ===
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
            # === END BaseEventLoop.run_forever() finally handling ===
        else:
            # Otherwise, live to tick another day. Enqueue the next tick,
            # and make sure there will be *something* to be processed.
            # If you don't ensure there is at least one message on the
            # queue, the select() call will block, locking the app.
            self.enqueue_tick()
            self.call_soon(self._loop_self_reading)
