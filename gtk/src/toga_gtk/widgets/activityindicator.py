from ..libs import GTK_VERSION, Gtk
from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = Gtk.Spinner()

    def is_running(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            return self.native.get_property("active")
        else:  # pragma: no-cover-if-gtk3
            return self.native.get_property("spinning")

    def start(self):
        self.native.start()

    def stop(self):
        self.native.stop()

    def rehint(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # print(
            #     "REHINT",
            #     self,
            #     self.native.get_preferred_width(),
            #     self.native.get_preferred_height(),
            # )
            width = self.native.get_preferred_width()[0]
            height = self.native.get_preferred_height()[0]
        else:  # pragma: no-cover-if-gtk3
            size = self.native.get_preferred_size()[1]
            width, height = size.width, size.height
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
