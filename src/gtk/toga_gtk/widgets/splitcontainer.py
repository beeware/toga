from ..libs import Gtk
from ..window import GtkViewport
from .base import Widget


class TogaSplitContainer(Gtk.Paned):
    def __init__(self, impl):
        Gtk.Paned.__init__(self)
        self._impl = impl
        self.interface = self._impl.interface

    def do_size_allocate(self, allocation):
        Gtk.Paned.do_size_allocate(self, allocation)

        # Turn all the weights into a fraction of 1.0
        total = sum(self.interface._weight)
        self.interface._weight = [weight/total for weight in self.interface._weight]

        # Set the position of splitter depending on the weight of splits.
        self.set_position(
            int(
                self.interface._weight[0] * self.get_allocated_width()
                if self.interface.direction == self.interface.VERTICAL
                else self.get_allocated_height()
            )
        )


class SplitContainer(Widget):
    def create(self):
        self.native = TogaSplitContainer(self)
        # Use Paned widget rather than VPaned and HPaned deprecated widgets
        # Note that orientation in toga behave unlike Gtk
        if self.interface.direction == self.interface.VERTICAL:
            self.native.set_orientation(Gtk.Orientation.HORIZONTAL)
        elif self.interface.direction == self.interface.HORIZONTAL:
            self.native.set_orientation(Gtk.Orientation.VERTICAL)
        else:
            raise ValueError("Allowed orientation is VERTICAL or HORIZONTAL")

        self.native.interface = self.interface

    def add_content(self, position, widget, flex):
        widget.viewport = GtkViewport(self.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        if position >= 2:
            raise ValueError('SplitContainer content must be a 2-tuple')

        if position == 0:
            self.native.set_wide_handle(True)
            widget_frame = Gtk.Frame()
            widget_frame.add(widget.native)
            self.native.pack1(widget_frame, flex, False)
        elif position == 1:
            self.native.set_wide_handle(True)
            widget_frame = Gtk.Frame()
            widget_frame.add(widget.native)
            self.native.pack2(widget_frame, flex, False)

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
