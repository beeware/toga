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
        if self.native:
            self._container.native.add(self.native)

    # def set_container(self, container):
    #     if self._impl:
    #         self._container._impl.add(self._impl)

    def add_child(self, child):
        if self._container:
            child._set_container(self._container)
        self.rehint()

    def apply_layout(self):
        pass

    def set_font(self, font):
        self.native.override_font(font._impl)

    def set_background_color(self, background_color):
        pass

    def rehint(self):
        for c in self.interface.children:
            c.rehint()
