from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = self._create_native_widget("sl-spinner")
        self.stop()

    # Actions
    def start(self):
        self.native.style.visibility = "visible"
        self._is_running = True

    def stop(self):
        self.native.style.visibility = "hidden"
        self._is_running = False

    def is_running(self):
        return self._is_running
