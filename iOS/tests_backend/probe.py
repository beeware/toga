import asyncio

from toga_iOS.libs import NSRunLoop, UIScreen


class BaseProbe:
    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # If we're running slow, wait for a second
        if self.app.run_slow:
            print("Waiting for redraw" if message is None else message)
            delay = 1

        if delay:
            await asyncio.sleep(delay)
        else:
            # Running at "normal" speed, we need to release to the event loop
            # for at least one iteration. `runUntilDate:None` does this.
            NSRunLoop.currentRunLoop.runUntilDate(None)

    def assert_image_size(self, image_size, size):
        # Retina displays render images at a higher resolution than their reported size.
        scale = int(UIScreen.mainScreen.scale)
        assert image_size == (size[0] * scale, size[1] * scale)
