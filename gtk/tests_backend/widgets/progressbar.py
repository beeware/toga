import asyncio

from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = Gtk.ProgressBar

    @property
    def is_determinate(self):
        return self.widget._impl._max is not None

    @property
    def is_animating_indeterminate(self):
        return not self.is_determinate and self.widget._impl._running

    @property
    def position(self):
        return self.native.get_fraction()

    async def wait_for_animation(self):
        # This is a Red code/Blue code thing. As the test is running async,
        # but we're invoking the "start" method synchronously, there's no
        # guarantee that the async animation task will actually run. We
        # explicitly wait_for the task to ensure it runs.
        if self.impl._task:
            try:
                await asyncio.wait_for(self.impl._task, 0.2)
            except asyncio.TimeoutError:
                # Timeout is the expected outcome, as the task will run until it is
                # cancelled.
                pass
