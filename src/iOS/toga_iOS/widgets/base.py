from toga_iOS.constraints import Constraints


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self._viewport = None
        self.constraints = None
        self.native = None
        self.create()
        self.interface.style.reapply()
        self.set_enabled(self.interface.enabled)

    def create(self):
        pass

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self.container:
            if container:
                raise RuntimeError('Already have a container')
            else:
                # existing container should be removed
                self.constraints = None
                self._container = None
                self.native.removeFromSuperview()
        elif container:
            # setting container
            self._container = container
            self._container.native.addSubview(self.native)
            if not self.constraints:
                self.add_constraints()
            self.constraints.container = container

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, viewport):
        self._viewport = viewport

    def set_enabled(self, value):
        self.native.enabled = self.interface.enabled

    def focus(self):
        self.interface.factory.not_implemented("Widget.focus()")

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        offset_y = 0
        if self.container:
            offset_y = self.container.viewport.statusbar_height
        elif self.viewport:
            offset_y = self.viewport.statusbar_height
        self.constraints.update(
            x, y + offset_y,
            width, height
        )

    def set_alignment(self, alignment):
        pass

    def set_hidden(self, hidden):
        if self.container:
            for view in self.container._impl.subviews:
                if view._impl:
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

    # INTERFACE

    def add_child(self, child):
        if self.viewport:
            # we are the the top level UIView
            child.container = self
        else:
            child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def add_constraints(self):
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.constraints = Constraints(self)

    def rehint(self):
        pass
