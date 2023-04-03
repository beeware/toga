from ..libs import Gtk
from .base import Widget


class Box(Widget):
    def create(self):
        self.min_width = None
        self.min_height = None
        self.native = Gtk.Box()
