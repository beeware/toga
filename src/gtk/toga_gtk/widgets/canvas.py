from gi.repository import Gtk
from .base import Widget


class Canvas(Widget):
    def create(self):
        self.native = Gtk.DrawingArea()
        self.native.interface = self.interface
