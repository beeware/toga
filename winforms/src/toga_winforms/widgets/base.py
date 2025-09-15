from abc import ABC, abstractmethod
from decimal import ROUND_HALF_EVEN, Decimal

from System.Drawing import (
    Point,
    Size,
    SystemColors,
)
from travertino.size import at_least

from toga.colors import TRANSPARENT, rgba
from toga_winforms.colors import (
    native_color,
    toga_color,
)


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
    def __init__(self, interface):
        self.interface = interface

        self._container = None
        self.native = None
        self.create()

        # Widgets that need to set a different default background_color should override
        # the _default_background_color attribute.
        #
        # Note: On Winforms, _default_background_color is set in the form of toga color,
        #       instead of the native Color. This is because we need to manually do the
        #       alpha blending, and the native Color class does not directly handle the
        #       alpha transparency in the same way.
        if not hasattr(self, "_default_background_color"):
            # If a widget hasn't specifically defined a default background color then
            # set the system assigned background color as the default background color
            # of the widget.
            self._default_background_color = toga_color(self.native.BackColor)

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

        # Background color needs to be reapplied on widget parent change as WinForms
        # doesn't actually support transparency. It just copies the parent's
        # BackColor to the widget. So, if a widget's parent changes then we need
        # to reapply background_color to copy the new parent's BackColor.
        self.set_background_color(self.interface.style.background_color)

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

    def set_text_align(self, alignment):
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
        if self.interface.parent:
            parent_color = toga_color(self.interface.parent._impl.native.BackColor).rgba
        else:
            parent_color = toga_color(SystemColors.Control).rgba

        if color is None:
            if self._default_background_color is TRANSPARENT:
                requested_color = rgba(0, 0, 0, 0)
            else:
                requested_color = self._default_background_color.rgba
        elif color is TRANSPARENT:
            requested_color = rgba(0, 0, 0, 0)
        else:
            requested_color = color.rgba

        blended_color = requested_color.blend_over(parent_color)
        self.native.BackColor = native_color(blended_color)

        for child in self.interface.children:
            child._impl.set_background_color(child.style.background_color)

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
