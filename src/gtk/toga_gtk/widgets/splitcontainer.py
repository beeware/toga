from gi.repository import Gtk

from toga_gtk.window import GtkViewport

from .base import Widget


class SplitContainer(Widget):
    def create(self):
        if self.interface.direction == self.interface.HORIZONTAL:
            self.native = Gtk.VPaned()
        else:
            self.native = Gtk.HPaned()
        self.native.interface = self.interface
        self.ratio = None

    def add_content(self, position, widget):
        widget.viewport = GtkViewport(self.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        if position >= 2:
            raise ValueError('SplitContainer content must be a 2-tuple')

        if position == 0:
            self.native.add1(widget.native)
        elif position == 1:
            self.native.add2(widget.native)

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
