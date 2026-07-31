import asyncio

from tests.conftest import approx

import toga
from toga_iOS.libs import NSRunLoop, UIScreen


class BaseProbe:
    async def redraw(self, message=None, delay=0, wait_for=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # If we're running slow, or we have a wait condition,
        # wait for at least a second
        if toga.App.app.run_slow or wait_for:
            delay = max(1, delay)

        print("Waiting for redraw" if message is None else message)
        if delay or wait_for:
            if toga.App.app.run_slow or wait_for is None:
                await asyncio.sleep(delay)
            else:
                delta = 0.1
                interval = 0.0
                while not wait_for() and interval < delay:
                    await asyncio.sleep(delta)
                    interval += delta

        else:
            # Running at "normal" speed, we need to release to the event loop
            # for at least one iteration. `runUntilDate:None` does this.
            NSRunLoop.currentRunLoop.runUntilDate(None)

    def assert_image_size(self, image_size, size, screen, window=None):
        # Retina displays render images at a higher resolution than their reported size.
        scale = int(UIScreen.mainScreen.scale)
        assert image_size == (
            approx(size[0] * scale, abs=2),
            approx(size[1] * scale, abs=2),
        )

    async def _wait_for_assertion(self, assertion, timeout=5, polling_interval=0.1):
        # Loop for up to `timeout` seconds, until assertion() passes without
        # raising an AssertionError
        loop = asyncio.get_running_loop()
        start_time = loop.time()
        while (loop.time() - start_time) < timeout:
            try:
                assertion()
                return
            except AssertionError as e:
                exception = e
                await asyncio.sleep(polling_interval)

        raise exception
