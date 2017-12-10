from gi.repository import Gtk


def wrapped_handler(widget, handler):
    def _handler(impl, data=None):
        if handler:
            return handler(widget)

    return _handler


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.constraints = None
        self.native = None
        self.create()

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
        if self.native:
            self._container.native.add(self.native)

        for child in self.interface.children:
            child._impl.container = container
        self.interface.rehint()

    @property
    def enabled(self):
        return self.native.get_sensitive()

    @enabled.setter
    def enabled(self, value):
        self.native.set_sensitive(value)

    def add_child(self, child):
        if self._container:
            child.container = self.container
        self.rehint()

    def apply_layout(self):
        pass

    def apply_sub_layout(self):
        pass

    def set_font(self, font):
        self.native.font = font._impl.native

    def set_background_color(self, background_color):
        pass

    def rehint(self):
        for c in self.interface.children:
            c.rehint()
