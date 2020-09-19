from ..libs import Gtk
from ..window import GtkViewport
from .base import Widget


class SplitContainer(Widget):
    def create(self):
        # Use Paned widget rather than VPaned and HPaned deprecated widgets
        # Note that orientation in toga behave unlike Gtk
        if self.interface.VERTICAL:
            self.native = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        elif self.interface.HORIZONTAL:
            self.native = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
        else:
            raise ValueError("Allowed orientation is VERTICAL or HORIZONTAL")

        self.native.interface = self.interface
        self.ratio = None

    def add_content(self, position, widget, flex):
        widget.viewport = GtkViewport(self.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        if position >= 2:
            raise ValueError('SplitContainer content must be a 2-tuple')

        if position == 0:
            self.native.set_wide_handle(True)
            self.native.pack1(widget.native, flex, False)
        elif position == 1:
            self.native.set_wide_handle(True)
            self.native.pack2(widget.native, flex, False)

    def set_app(self, app):
        if self.interface.content:
            self.interface.content[0].app = self.interface.app
            self.interface.content[1].app = self.interface.app

    def set_window(self, window):
        if self.interface.content:
            self.interface.content[0].window = self.interface.window
            self.interface.content[1].window = self.interface.window

    def set_direction(self, value):
        self.interface.factory.not_implemented('SplitContainer.set_direction()')
