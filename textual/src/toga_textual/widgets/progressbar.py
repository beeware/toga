from textual.widgets import ProgressBar as TextualProgressBar
from travertino.size import at_least

from .base import Widget


class TogaProgressBar(TextualProgressBar, can_focus=True):
    pass


class ProgressBar(Widget):
    def create(self):
        self.native = TogaProgressBar(
            total=1.0,
            show_percentage=False,
            show_eta=False,
        )
        self._max = 1.0
        self._running = False

    def is_running(self):
        return self._running

    def get_value(self):
        if self._max is None:
            return None
        return self.native.progress

    def set_value(self, value):
        self.native.update(progress=value)

    def get_max(self):
        return self._max

    def set_max(self, value):
        if value is None:
            self._max = None
            self.native.update(total=None, progress=0)
        else:
            if self._max is None:
                self.native.update(total=value, progress=0)
            else:
                self.native.update(total=value)
            self._max = value

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def rehint(self):
        self.interface.intrinsic.width = at_least(
            self.scale_in_horizontal(self.interface._MIN_WIDTH)
        )
        self.interface.intrinsic.height = 1
