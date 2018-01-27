from gi.repository import Gtk
from travertino.size import at_least


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.viewport = None
        self.native = None
        self.create()
        self.interface.style.reapply()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
        self._container.native.add(self.native)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.native.set_sensitive(value)

    ### APPLICATOR

    def set_bounds(self, x, y, width, height):
        # No implementation required here; the new sizing will be picked up
        # by the box's allocation handler.
        pass

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        self.interface.factory.not_implemented('Widget.set_hidden()')

    def set_font(self, font):
        # By default, fon't can't be changed
        pass

    def set_color(self, color):
        # By default, color can't be changed
        pass

    def set_background_color(self, color):
        # By default, background color can't be changed
        pass

    ### INTERFACE

    def add_child(self, child):
        if self.container:
            child.container = self.container

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = at_least(height[0])
