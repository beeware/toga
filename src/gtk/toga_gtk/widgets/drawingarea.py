from gi.repository import Gtk
from .base import Widget


class DrawingArea(Widget):
    def create(self):
        self.native = Gtk.DrawingArea()
        self.native.interface = self.interface
