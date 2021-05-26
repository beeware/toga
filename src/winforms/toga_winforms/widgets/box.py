from travertino.constants import TRANSPARENT

from toga_winforms.colors import native_color
from toga_winforms.libs import Point, Size, WinForms

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()
        self.native.interface = self.interface

    def set_bounds(self, x, y, width, height):
        if self.native:
            vertical_shift = 0
            try:
                # If the box is the outer widget, we need to shift it to the frame vertical_shift
                vertical_shift = self.frame.vertical_shift - self.interface.style.padding_top
            except AttributeError:
                vertical_shift = self.interface.style.padding_top
            horizontal_shift = self.interface.style.padding_left
            horizontal_size_adjustment = self.interface.style.padding_right + horizontal_shift
            vertical_size_adjustment = self.interface.style.padding_bottom
            self.native.Size = Size(width + horizontal_size_adjustment, height + vertical_size_adjustment)
            self.native.Location = Point(x - horizontal_shift, y + vertical_shift)

    def set_background_color(self, value):
        if value:
            self.native.BackColor = native_color(value)
        else:
            self.native.BackColor = native_color(TRANSPARENT)
