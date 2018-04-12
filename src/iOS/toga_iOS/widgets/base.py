from toga_iOS.constraints import Constraints


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.constraints = None
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
        if self.constraints:
            self._container.native.addSubview(self.native)
            self.constraints.container = container

        for child in self.interface.children:
            child._impl.container = container
        self.rehint()

    def set_enabled(self, value):
        self.native.enabled = value

    ### APPLICATOR

    def set_bounds(self, x, y, width, height):
        if self.container:
            viewport = self.container.viewport
        else:
            viewport = self.viewport

        self.constraints.update(
            x, y + viewport.statusbar_height,
            width, height
        )

    def set_alignment(self, alignment):
        pass

    def set_hidden(self, hidden):
        if self._container:
            for view in self._container._impl.subviews:
                if child._impl == view:
                    view.setHidden(hidden)

    def set_font(self, font):
        # By default, font can't be changed
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
            child.viewport = self.root.viewport
            child.container = self.container

    def add_constraints(self):
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.constraints = Constraints(self)

    def rehint(self):
        pass
