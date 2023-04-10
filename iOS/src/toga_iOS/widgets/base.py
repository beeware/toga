from abc import abstractmethod

from toga.colors import TRANSPARENT
from toga_iOS.colors import native_color
from toga_iOS.constraints import Constraints
from toga_iOS.libs import UIColor


class Widget:
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self._viewport = None
        self.constraints = None
        self.native = None
        self.create()
        self.interface.style.reapply()

    @abstractmethod
    def create(self):
        ...

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
            assert container is None, "Widget already has a container"

            # Existing container should be removed
            self.constraints.container = None
            self._container = None
            self.native.removeFromSuperview()
        elif container:
            # setting container
            self._container = container
            self._container.native.addSubview(self.native)
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

    def get_enabled(self):
        return self.native.isEnabled()

    def set_enabled(self, value):
        self.native.enabled = value

    def focus(self):
        self.native.becomeFirstResponder()

    def get_tab_index(self):
        self.interface.factory.not_implemented("Widget.get_tab_index()")

    def set_tab_index(self, tab_index):
        self.interface.factory.not_implemented("Widget.set_tab_index()")

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        # print("SET BOUNDS", self, x, y, width, height, self.constraints)
        offset_y = 0
        if self.container:
            offset_y = self.container.viewport.top_offset
        elif self.viewport:
            offset_y = self.viewport.top_offset
        self.constraints.update(x, y + offset_y, width, height)

    def set_alignment(self, alignment):
        pass

    def set_hidden(self, hidden):
        self.native.setHidden(hidden)

    def set_font(self, font):
        # By default, font can't be changed
        pass

    def set_color(self, color):
        # By default, color can't be changed
        pass

    def set_background_color(self, color):
        # By default, background color can't be changed
        pass

    # TODO: check if it's safe to make this the default implementation.
    def set_background_color_simple(self, value):
        if value and (value != TRANSPARENT):
            self.native.backgroundColor = native_color(value)
        else:
            try:
                # systemBackgroundColor() was introduced in iOS 13
                # We don't test on iOS 12, so mark the other branch as nocover
                self.native.backgroundColor = UIColor.systemBackgroundColor()
            except AttributeError:  # pragma: no cover
                self.native.backgroundColor = UIColor.whiteColor

    # INTERFACE

    def add_child(self, child):
        if self.viewport:
            # we are the top level UIView
            child.container = self
        else:
            child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def add_constraints(self):
        self.constraints = Constraints(self)
        self.native.translatesAutoresizingMaskIntoConstraints = False

    def refresh(self):
        self.rehint()

    @abstractmethod
    def rehint(self):
        ...
