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

    def apply_sub_layout(self):
        """ Force a layout update on the widget.
        """
        if self.interface.content and self.native.is_visible():
            if self.interface.direction == self.interface.VERTICAL:
                size = self.native.get_allocation().width
                if self.ratio is None:
                    self.ratio = 0.5
                    self.native.set_position(size * self.ratio)
                self.containers[0].interface._update_layout(width=size * self.ratio)
                self.containers[1].interface._update_layout(width=size * (1.0 - self.ratio))
            else:
                size = self.native.get_allocation().height
                if self.ratio is None:
                    self.ratio = 0.5
                    self.native.set_position(size * self.ratio)
                self.containers[0].interface._update_layout(height=size * self.ratio)
                self.containers[1].interface._update_layout(height=size * (1.0 - self.ratio))
