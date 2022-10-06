
class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None

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

        for child in self.interface.children:
            child._impl.container = container

    def set_enabled(self, value):
        self.native.set_sensitive(self.interface.enabled)

    def focus(self):
        self.interface.factory.not_implemented("Widget.focus()")

    ######################################################################
    # APPLICATOR
    #
    # Web style is a little different to other platforms; we if there's
    # any change, we can just re-set the CSS styles and the browser
    # will reflect those changes as needed.
    ######################################################################

    def set_bounds(self, x, y, width, height):
        self.native.style = self.interface.style.__css__()

    def set_alignment(self, alignment):
        self.native.style = self.interface.style.__css__()

    def set_hidden(self, hidden):
        self.native.style = self.interface.style.__css__()

    def set_font(self, font):
        self.native.style = self.interface.style.__css__()

    def set_color(self, color):
        self.native.style = self.interface.style.__css__()

    def set_background_color(self, color):
        self.native.style = self.interface.style.__css__()

    ######################################################################
    # INTERFACE
    ######################################################################

    def add_child(self, child):
        pass

    def rehint(self):
        pass
