
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
        if self.constraints and self.native:
            self._container.native.addSubview_(self.native)
            self.constraints.container = container

        for child in self.interface.children:
            child._impl.container = container
        self.interface.rehint()

    def set_enabled(self, value):
        self.native.enabled = value

    ### APPLICATOR

    def set_bounds(self, x, y, width, height):
        self._action('set bounds', x=x, y=y, width=width, height=height)

    def set_hidden(self, hidden):
        self._action('set hidden', hidden=hidden)

    def set_font(self, font):
        self._action('set font', font=font)

    def set_background_color(self, color):
        self._action('set background color', color=color)

    ### INTERFACE

    def add_child(self, child):
        if self._container:
            child._set_container(self._container)

    def rehint(self):
        pass
