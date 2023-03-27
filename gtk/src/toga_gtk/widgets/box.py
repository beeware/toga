from ..libs import Gtk
from .base import Widget


class Box(Widget):
    def create(self):
        self.min_width = None
        self.min_height = None
        self.native = Gtk.Box()
        self.native.set_name(f"toga-{self.interface.id}")
        self.native.get_style_context().add_class("toga")
        self.native._impl = self
        self.native.interface = self.interface
