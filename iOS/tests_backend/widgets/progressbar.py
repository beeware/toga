import asyncio

from toga_iOS.libs import UIProgressView

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = UIProgressView

    @property
    def is_determinate(self):
        return self.widget._impl._max is not None

    @property
    def is_animating_indeterminate(self):
        return self.widget._impl._task is not None

    @property
    def position(self):
        return self.native.progress

    async def wait_for_animation(self):
        # We need to enforce a short sleep here because iOS implements it's own
        # animation as a background task, and we need to give that animation time to
        # run.
        await asyncio.sleep(0.1)
