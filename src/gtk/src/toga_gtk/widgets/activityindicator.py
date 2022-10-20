from ..libs import Gtk
from .base import Widget


class ActivityIndicator(Widget):

    def create(self):
        self.native = Gtk.Spinner()
        self.native.interface = self.interface

    def start(self):
        self.native.start()

    def stop(self):
        self.native.stop()
