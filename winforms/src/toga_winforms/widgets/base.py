from abc import abstractmethod

from toga_winforms.colors import native_color
from toga_winforms.libs import Color, Point, Size, SystemColors


class Widget:
    # In some widgets, attempting to set a background color with any alpha value other
    # than 1 raises "System.ArgumentException: Control does not support transparent
    # background colors". Those widgets should set this attribute to False.
    _background_supports_alpha = True

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.native = None
        self.create()
        self.scale = self.native.CreateGraphics().DpiX / 96
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
        if self._container:
            self._container.remove_content(self)

        self._container = container
        if container:
            container.add_content(self)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    @property
    def viewport(self):
        return self._container

    # Convert CSS pixels to native pixels
    def scale_in(self, value):
        return int(round(value * self.scale))

    # Convert native pixels to CSS pixels
    def scale_out(self, value):
        return int(round(value / self.scale))

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

    def set_bounds(self, x, y, width, height):
        self.native.Size = Size(width, height)
        self.native.Location = Point(x, y)

    def set_alignment(self, alignment):
        # By default, alignment can't be changed
        pass

    def set_hidden(self, hidden):
        self.native.Visible = not hidden

    def set_font(self, font):
        self.native.Font = font._impl.native

    def set_color(self, color):
        if color is None:
            self.native.ForeColor = SystemColors.WindowText
        else:
            self.native.ForeColor = native_color(color)

    def set_background_color(self, color):
        if not hasattr(self, "_default_background"):
            self._default_background = self.native.BackColor
        if color is None:
            self.native.BackColor = self._default_background
        else:
            win_color = native_color(color)
            if (win_color != Color.Empty) and (not self._background_supports_alpha):
                win_color = Color.FromArgb(255, win_color.R, win_color.G, win_color.B)
            self.native.BackColor = win_color

    # INTERFACE

    def add_child(self, child):
        child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def refresh(self):
        self.rehint()

    @abstractmethod
    def rehint(self):
        ...
