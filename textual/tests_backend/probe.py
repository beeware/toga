import asyncio

import pytest
from textual._wait import wait_for_idle
from textual.app import ScreenStackError

import toga


class BaseProbe:
    HORIZONTAL_SCALE = 800 // 80
    VERTICAL_SCALE = 600 // 25

    def approx_width(self, width):
        return pytest.approx(width, abs=self.HORIZONTAL_SCALE // 2)

    def approx_height(self, height):
        return pytest.approx(height, abs=self.VERTICAL_SCALE // 2)

    async def _wait_for_screen(self, timeout=5.0):
        """Wait until the screen and all its child widgets have processed the
        messages currently in their queues.

        This duplicates the approach used by Textual's own `Pilot._wait_for_screen`.
        """
        native = self.app._impl.native
        try:
            screen = native.screen
        except ScreenStackError:
            return

        children = [native, *screen.walk_children(with_self=True)]
        count = 0
        count_zero_event = asyncio.Event()

        def decrement_counter():
            """Decrement internal counter, and set an event if it reaches zero."""
            nonlocal count
            count -= 1
            if count == 0:
                # When count is zero, all messages queued at the start of the
                # method have been processed.
                count_zero_event.set()

        for child in children:
            if child.call_later(decrement_counter):
                count += 1

        if count:
            # Wait for the count to return to zero, or a timeout, or an exception
            wait_for = [
                asyncio.ensure_future(count_zero_event.wait()),
                asyncio.ensure_future(native._exception_event.wait()),
            ]
            _, pending = await asyncio.wait(
                wait_for,
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()

            timed_out = len(wait_for) == len(pending)
            if timed_out:
                pytest.fail(
                    "Timed out while waiting for widgets to process pending messages."
                )

    async def redraw(self, message=None, delay=0, wait_for=None):
        # This implementation is strongly inspired by Textual's Pilot.pause(),
        # but adding `wait_for` handling.
        if toga.App.app.run_slow or wait_for:
            delay = max(1, delay)

        print("Waiting for redraw" if message is None else message)
        await self._wait_for_screen()
        await wait_for_idle(0)
        if delay or wait_for:
            if toga.App.app.run_slow or wait_for is None:
                await asyncio.sleep(delay)
            else:
                delta = 0.1
                interval = 0.0
                while not wait_for() and interval < delay:
                    await asyncio.sleep(delta)
                    interval += delta

        self.app._impl.native.screen._on_timer_update()

    def assert_image_size(self, image_size, size, screen, window=None):
        pytest.skip("Image size assertions are not implemented on Textual.")
