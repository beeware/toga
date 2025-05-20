import asyncio

import toga
from toga_gtk.libs import GTK_VERSION, GLib, Gtk


class BaseProbe:
    def repaint_needed(self):
        if GTK_VERSION < (4, 0, 0):
            return Gtk.events_pending()
        else:
            return GLib.main_context_default().pending()

    async def redraw(self, message=None, delay=0):
        """Request a redraw of the app, waiting until that redraw has completed."""
        print(f"[DEBUG REDRAW] Redraw called with message: {message}, delay: {delay}")
        if (
            hasattr(self, "native")
            and self.native
            and hasattr(self.native, "queue_draw")
        ):
            print(
                f"[DEBUG REDRAW] Native widget available, "
                f"calling queue_draw on {self.native}"
            )
            self.native.queue_draw()

        print("[DEBUG REDRAW] Processing events to ensure UI is fully updated")
        events_processed = 0
        for i in range(15):
            if GTK_VERSION < (4, 0, 0):
                if Gtk.events_pending():
                    Gtk.main_iteration_do(blocking=False)
                else:
                    break
            else:
                context = GLib.main_context_default()
                if context.pending():
                    print(f"[DEBUG REDRAW] GTK4: Processing context iteration {i+1}")
                    context.iteration(may_block=False)
                    events_processed += 1
                else:
                    print(
                        f"[DEBUG REDRAW] GTK4: "
                        f"No more events pending after {events_processed} iterations"
                    )
                    break

        # Always yield to let GTK catch up
        print("[DEBUG REDRAW] Yielding control with asyncio.sleep(0)")
        await asyncio.sleep(0)
        print("[DEBUG REDRAW] Redraw method complete")

        if toga.App.app.run_slow:
            delay = max(1, delay)
        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert image_size == size
