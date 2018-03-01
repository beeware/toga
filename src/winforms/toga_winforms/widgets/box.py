from toga_winforms.libs import WinForms, Color, Size, Point

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()
        self.native.interface = self.interface

    def set_bounds(self, x, y, width, height):
        if self.native:
            vertical_shift = self.interface.style.padding_top
            horizontal_shift = self.interface.style.padding_left
            horizontal_size_adjustment = self.interface.style.padding_right + horizontal_shift
            vertical_size_adjustment = self.interface.style.padding_bottom + vertical_shift
            self.native.Size = Size(width + horizontal_size_adjustment, height + vertical_size_adjustment)
            self.native.Location = Point(x - horizontal_shift, y - vertical_shift)
