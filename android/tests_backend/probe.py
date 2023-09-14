import asyncio


class BaseProbe:
    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # If we're running slow, wait for a second
        if self.app.run_slow:
            delay = 1

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)
