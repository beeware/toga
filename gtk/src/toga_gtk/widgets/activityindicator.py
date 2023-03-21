from ..libs import Gtk
from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = Gtk.Spinner()
        self.native.set_name(f"toga-{self.interface.id}")
        self.native.get_style_context().add_class("toga")
        self.native.interface = self.interface

    def is_running(self):
        return self.native.get_property("active")

    def start(self):
        self.native.start()

    def stop(self):
        self.native.stop()

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = width[0]
        self.interface.intrinsic.height = height[0]
