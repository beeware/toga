"""
A web widget to display an activity indicator.

This is a web implementation of the `toga.ActivityIndicator` widget.

Details can be found in
https://shoelace.style/components/spinner
"""
from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.interface.style._use_default_width = False
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
