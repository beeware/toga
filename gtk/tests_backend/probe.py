import asyncio

import toga
from toga_gtk.libs import GLib


class BaseProbe:
    async def redraw(self, message=None, delay=0):
        # Process events to ensure the UI is fully updated
        context = GLib.main_context_default()
        while context.pending():
            context.iteration(may_block=False)

        # Always yield to let GTK catch up
        await asyncio.sleep(0)

        if toga.App.app.run_slow:
            delay = max(1, delay)
        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert image_size == size
