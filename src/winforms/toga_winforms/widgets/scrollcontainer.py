from toga_winforms.libs import WinForms
from toga_winforms.window import WinFormsViewport

from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = WinForms.Panel()
        self.native.interface = self.interface
        self.native.AutoScroll = True
        self.native.Scroll += self.winforms_scroll
        self.native.MouseWheel += self.winforms_scroll

    def winforms_scroll(self, sender, event):
        if self.interface.on_scroll is not None:
            self.interface.on_scroll(self.interface)

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

    def set_on_scroll(self, on_scroll):
        # Do nothing
        pass

    def get_vertical_position(self):
        return self.native.VerticalScroll.Value / self.native.VerticalScroll.Maximum

    def set_vertical_position(self, vertical_position):
        new_value = int(vertical_position * self.native.VerticalScroll.Maximum)
        self.native.VerticalScroll.Value = new_value
        if self.interface.on_scroll is not None:
            self.interface.on_scroll(self.interface)

    def get_horizontal_position(self):
        return self.native.HorizontalScroll.Value / self.native.HorizontalScroll.Maximum

    def set_horizontal_position(self, horizontal_position):
        new_value = int(horizontal_position * self.native.HorizontalScroll.Maximum)
        self.native.HorizontalScroll.Value = new_value
        if self.interface.on_scroll is not None:
            self.interface.on_scroll(self.interface)
