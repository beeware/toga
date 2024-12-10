from abc import ABC, abstractmethod
from decimal import ROUND_HALF_EVEN, Decimal

from System.Drawing import (
    Color,
    Point,
    Size,
    SystemColors,
)
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_winforms.colors import native_color


class Scalable(ABC):
    SCALE_DEFAULT_ROUNDING = ROUND_HALF_EVEN

    @property
    @abstractmethod
    def dpi_scale(self):
        raise NotImplementedError()

    # Convert CSS pixels to native pixels
    def scale_in(self, value, rounding=SCALE_DEFAULT_ROUNDING):
        return self.scale_round(value * self.dpi_scale, rounding)

    # Convert native pixels to CSS pixels
    def scale_out(self, value, rounding=SCALE_DEFAULT_ROUNDING):
        if isinstance(value, at_least):
            return at_least(self.scale_out(value.value, rounding))
        else:
            return self.scale_round(value / self.dpi_scale, rounding)

    def scale_round(self, value, rounding):
        if rounding is None:
            return value
        return int(Decimal(value).to_integral(rounding))


class Widget(Scalable, ABC):
    # In some widgets, attempting to set a background color with any alpha value other
    # than 1 raises "System.ArgumentException: Control does not support transparent
    # background colors". Those widgets should set this attribute to False.
    _background_supports_alpha = True

    def __init__(self, interface):
        self.interface = interface

        self._container = None
        self.native = None
        self.create()

        # Obtain a Graphics object and immediately dispose of it. This is
        # done to trigger the control's Paint event and force it to redraw.
        # Since in toga, Hwnds could be created at inappropriate times.
        # As an example, without this fix, running the OptionContainer
        # example app should give an error, like:
        #
        # System.ArgumentOutOfRangeException: InvalidArgument=Value of '0' is not valid
        # for 'index'.
        # Parameter name: index
        #    at System.Windows.Forms.TabControl.GetTabPage(Int32 index)
        self.native.CreateGraphics().Dispose()

    @abstractmethod
    def create(self): ...

    def set_app(self, app):
        # No special handling required
        pass

    def set_window(self, window):
        self.scale_font()

    @property
    def dpi_scale(self):
        window = self.interface.window
        if window:
            return window._impl.dpi_scale
        else:
            return 1

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

        self.refresh()

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
        self.native.Size = Size(*map(self.scale_in, (width, height)))
        self.native.Location = Point(*map(self.scale_in, (x, y)))

    def set_text_alignment(self, alignment):
        # By default, text alignment can't be changed
        pass

    def set_hidden(self, hidden):
        self.native.Visible = not hidden

    def set_font(self, font):
        self.original_font = font._impl.native
        self.scale_font()

    def scale_font(self):
        font = self.original_font
        window = self.interface.window
        if window:
            font = window._impl.scale_font(self.original_font)
        self.native.Font = font

    def set_color(self, color):
        if color is None:
            self.native.ForeColor = SystemColors.WindowText
        else:
            self.native.ForeColor = native_color(color)

    def set_background_color(self, color):
        if not hasattr(self, "_default_background"):
            self._default_background = self.native.BackColor
        if color is None or (
            color == TRANSPARENT and not self._background_supports_alpha
        ):
            self.native.BackColor = self._default_background
        else:
            win_color = native_color(color)
            if not self._background_supports_alpha:
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
        # Default values; may be overwritten by rehint().
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
        self.rehint()

    def rehint(self):
        pass
