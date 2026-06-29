from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = self._create_native_widget("wa-spinner")
        self.stop()

    # Actions
    def start(self):
        self.native.classList.remove("stopped")
        self._is_running = True

    def stop(self):
        self.native.classList.add("stopped")
        self._is_running = False

    def is_running(self):
        return self._is_running
