from abc import abstractmethod

from toga_iOS.colors import native_color
from toga_iOS.constraints import Constraints


class Widget:
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self._container = None
        self.constraints = None
        self.native = None
        self.create()

        # Many widgets have a "transparent" background; however, some widgets use
        # UIColor.ClearColor, and some use UIExtendedGrayColorSpace 0 0, which has
        # slightly different color mixing characteristics. Widgets like TextInput use
        # `None` as their initial background color, so that always adapts to light/dark
        # mode. Preserve the initial background color on the freshly created widget so
        # that we can reset back to that color when background_color is set to None. See
        # #3104 for details.
        self._default_background_color = self.native.backgroundColor

    @abstractmethod
    def create(self): ...

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
            assert container is None, f"{self} already has a container"

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

    def get_enabled(self):
        return self.native.isEnabled()

    def set_enabled(self, value):
        self.native.setEnabled(value)

    @property
    def has_focus(self):
        return self.native.isFirstResponder

    def focus(self):
        if not self.has_focus:
            self.native.becomeFirstResponder()

    def get_tab_index(self):
        self.interface.factory.not_implemented("Widget.get_tab_index()")

    def set_tab_index(self, tab_index):
        self.interface.factory.not_implemented("Widget.set_tab_index()")

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        # print("SET BOUNDS", self, x, y, width, height, self.container.top_offset)
        self.constraints.update(x, y + self.container.top_offset, width, height)

    def set_text_align(self, alignment):
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
        self.native.backgroundColor = (
            self._default_background_color if color is None else native_color(color)
        )

    # INTERFACE
    def add_child(self, child):
        child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def add_constraints(self):
        self.constraints = Constraints(self)

    def refresh(self):
        self.rehint()

    @abstractmethod
    def rehint(self): ...
