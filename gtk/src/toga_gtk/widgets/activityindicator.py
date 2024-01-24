from ..libs import Gtk
from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = Gtk.Spinner

    def is_running(self):
        return self.native.get_spinning()

    def start(self):
        self.native.start()

    def stop(self):
        self.native.stop()

    def rehint(self):
        # print(
        #     "REHINT",
        #     self,
        #     self.native.get_preferred_size()[0].width,
        #     self.native.get_preferred_size()[0].height,
        # )
        min_size, _ = self.native.get_preferred_size()

        self.interface.intrinsic.width = min_size.width
        self.interface.intrinsic.height = min_size.height
