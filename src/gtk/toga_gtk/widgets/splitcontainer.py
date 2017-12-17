from gi.repository import Gtk

from toga_gtk.container import Container

from .base import Widget


class SplitContainer(Widget):
    def create(self):
        if self.interface.direction == self.interface.HORIZONTAL:
            self.native = Gtk.VPaned()
        else:
            self.native = Gtk.HPaned()
        self.native.interface = self.interface
        self.ratio = None
        self.containers = []

    def add_content(self, position, widget):
        if widget.native is None:
            container = Container()
            container.content = widget
        else:
            container = widget

        widget.viewport = CocoaViewport(widget.native)

        self.containers.append(container)

        if position >= 2:
            raise ValueError('SplitContainer content must be a 2-tuple')

        if position == 0:
            add = self.native.add1
        elif position == 1:
            add = self.native.add2

        add(container.native)

    def set_app(self, app):
        if self.interface.content:
            self.interface.content[0].app = self.interface.app
            self.interface.content[1].app = self.interface.app

    def set_window(self, window):
        if self.interface.content:
            self.interface.content[0].window = self.interface.window
            self.interface.content[1].window = self.interface.window

    def set_direction(self, value):
        pass
