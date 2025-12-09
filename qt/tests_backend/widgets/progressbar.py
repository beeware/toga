import asyncio

from PySide6.QtWidgets import QProgressBar

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = QProgressBar

    @property
    def is_determinate(self):
        return not self.widget._impl._indeterminate

    @property
    def is_animating_indeterminate(self):
        return (
            self.widget._impl.native.minimum() == 0
            and self.widget._impl.native.maximum() == 0
        )

    @property
    def position(self):
        return self.native.value() / 100

    async def wait_for_animation(self):
        # We need to enforce a short sleep here because Qt implements it's own
        # animation as a background task, and we need to give that animation time to
        # run.
        await asyncio.sleep(0.1)
