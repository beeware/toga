from abc import abstractmethod

from toga_winforms.colors import native_color
from toga_winforms.libs import Point, Size, SystemColors


class Widget:
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.native = None
        self.viewport = None
        self.create()
        self.interface.style.reapply()

    @abstractmethod
    def create(self):
        ...

    def set_app(self, app):
        # No special handling required
        pass

    def set_window(self, window):
        # No special handling required
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self.container:
            assert container is None, "Widget already has a container"
            # container is set to None, removing self from the container.native
            self._container.native.Controls.Remove(self.native)
            self._container = None
        elif container:
            # setting container, adding self to container.native
            self._container = container
            self._container.native.Controls.Add(self.native)
            self.native.BringToFront()

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    @property
    def viewport(self):
        return self._viewport

    @viewport.setter
    def viewport(self, viewport):
        self._viewport = viewport

    def get_tab_index(self):
        return self.native.TabIndex

    def set_tab_index(self, tab_index):
        self.native.TabIndex = tab_index

    def get_enabled(self):
        return self.native.Enabled

    def set_enabled(self, value):
        self.native.Enabled = value

    def focus(self):
        self.native.Focus()

    # APPLICATOR

    @property
    def vertical_shift(self):
        return 0

    def set_bounds(self, x, y, width, height):
        # Root level widgets may require vertical adjustment to
        # account for toolbars, etc.
        if self.interface.parent is None:
            vertical_shift = self.frame.vertical_shift
        else:
            vertical_shift = 0

        self.native.Size = Size(width, height)
        self.native.Location = Point(x, y + vertical_shift)

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        self.native.Visible = not hidden

    def set_font(self, font):
        # By default, font can't be changed
        pass

    def set_color(self, color):
        if color is None:
            self.native.ForeColor = SystemColors.WindowText
        else:
            self.native.ForeColor = native_color(color)

    def set_background_color(self, color):
        if color is None:
            self.native.BackColor = SystemColors.Control
        else:
            self.native.BackColor = native_color(color)

    # INTERFACE

    def add_child(self, child):
        if self.viewport:
            # we are the top level container
            child.container = self
        else:
            child.container = self.container

    def insert_child(self, index, child):
        if self.viewport:
            # we are the the top level container
            child.container = self
        else:
            child.container = self.container

    def remove_child(self, child):
        child.container = None

    def refresh(self):
        self.rehint()

    @abstractmethod
    def rehint(self):
        ...
