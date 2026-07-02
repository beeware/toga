from textual.widgets import LoadingIndicator as TextualLoadingIndicator

from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = TextualLoadingIndicator()
        self._hidden = False
        self._running = False
        self.native.visible = False

    def set_hidden(self, hidden):
        self._hidden = hidden
        self.native.visible = self._running and not hidden

    def is_running(self):
        return self._running

    def start(self):
        self._running = True
        self.native.visible = not self._hidden

    def stop(self):
        self._running = False
        self.native.visible = False

    def rehint(self):
        self.interface.intrinsic.width = 2
        self.interface.intrinsic.height = 1
