from .base import Widget


class ProgressBar(Widget):
    def __init__(self, id=None, style=None, max=None, value=None):
        super().__init__(id=None, style=None)
        self._value = value
        self._running = False
