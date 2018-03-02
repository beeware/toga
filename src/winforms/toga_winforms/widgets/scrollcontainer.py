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

        widget.viewport = WinFormsViewport(self.native, self)
        widget.frame = self

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
