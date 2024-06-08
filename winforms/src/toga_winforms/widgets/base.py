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
    alpha_blending_over_operation,
    native_color,
    toga_color,
)


class Scalable:
    SCALE_DEFAULT_ROUNDING = ROUND_HALF_EVEN

    def init_scale(self, native):
        self.dpi_scale = native.CreateGraphics().DpiX / 96

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


class Widget(ABC, Scalable):

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self._container = None
        self.native = None

        # Widgets that need to set a different default background_color
        # should override this attribute.
        self._default_background_color = toga_color(SystemColors.Control)

        self.create()
        self.init_scale(self.native)
        self.interface.style.reapply()

    @abstractmethod
    def create(self): ...

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
        if color is None:
            if self._default_background_color != TRANSPARENT:
                self.native.BackColor = native_color(self._default_background_color)
            else:
                color = self._default_background_color
        elif (color != TRANSPARENT) and (color.a == 1):
            self.native.BackColor = native_color(color)
        else:
            if self.interface.parent:
                parent_color = toga_color(
                    self.interface.parent._impl.native.BackColor
                ).rgba
            else:
                parent_color = toga_color(SystemColors.Control).rgba

            if color is TRANSPARENT:
                requested_color = rgba(0, 0, 0, 0)
            else:
                requested_color = color.rgba

            blended_color = alpha_blending_over_operation(requested_color, parent_color)
            self.native.BackColor = native_color(blended_color)

        if getattr(self.interface, "children", None) is not None:  # pragma: no branch
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
        # Background color needs to be reapplied on widget refresh as WinForms
        # doesn't actually support transparency. It just copies the parent's
        # BackColor to the widget. So, if a widget's parent changes then we need
        # to reapply background_color to copy the new parent's BackColor.
        self.set_background_color(self.interface.style.background_color)

    def rehint(self):
        pass
