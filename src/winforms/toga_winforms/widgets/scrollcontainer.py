from travertino.size import at_least

from toga_winforms.libs import WinForms, Size, Point
from toga_winforms.window import WinFormsViewport

from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = WinForms.Panel()
        self.native.interface = self.interface
        self.native.AutoScroll = True

    def set_content(self, widget):
        self.inner_container = widget
        widget.viewport = WinFormsViewport(self.native)
        for child in widget.interface.children:
            child._impl.container = widget
        self.native.Controls.Add(self.inner_container.native)

    def set_horizontal(self, value):
        self.native.AutoScroll = False
        self.native.HorizontalScroll.Enabled = value
        self.native.HorizontalScroll.Visible = value
        self.native.AutoScroll = True

    def set_vertical(self, value):
        self.native.AutoScroll = False
        self.native.VerticalScroll.Enabled = value
        self.native.VerticalScroll.Visible = value
        self.native.AutoScroll = True

    def set_app(self, app):
        if self.interface.content:
            self.interface.content.app = app

    def set_window(self, window):
        if self.interface.content:
            self.interface.content.window = window

    @property
    def vertical_shift(self):
        vertical_shift = 0
        try:
            if self.interface.window:
                if self.interface.window.content == self.interface:
                    vertical_shift = self.interface.window._impl.toolbar_native.Height
            return vertical_shift
        except AttributeError:
            return vertical_shift

    def set_bounds(self, x, y, width, height):
        # Containers accommodate vertical_shift to take into account the
        # toolbar height
        if self.native:
            self.native.Size = Size(width, height)
            self.native.Location = Point(x, y + self.vertical_shift)
