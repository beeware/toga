import asyncio

from textual.widgets import ProgressBar as TextualProgressBar

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = TextualProgressBar

    @property
    def is_animating_indeterminate(self):
        return self.widget.is_running and self.native.percentage is None

    @property
    def position(self):
        return self.native.percentage

    async def wait_for_animation(self):
        await asyncio.sleep(0.1)
