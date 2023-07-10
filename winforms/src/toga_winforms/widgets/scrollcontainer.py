from toga_winforms.container import Container
from toga_winforms.libs import WinForms

from .base import Widget


class ScrollContainer(Widget, Container):
    def create(self):
        self.native = WinForms.Panel()
        self.native.AutoScroll = True
        self.native.Scroll += self.winforms_scroll
        self.native.MouseWheel += self.winforms_scroll
        self.init_container(self.native)

    def winforms_scroll(self, sender, event):
        self.interface.on_scroll(None)

    def resize_content(self):
        client_size = self.native.ClientSize  # Size not including scroll bars
        super().resize_content(client_size.Width, client_size.Height)
        if self.interface.content:
            self.interface.content.refresh()

        self.native.HorizontalScroll.Maximum = max(
            0, self.native_content.Width - client_size.Width
        )
        self.native.VerticalScroll.Maximum = max(
            0, self.native_content.Height - client_size.Height
        )

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.resize_content()

    def get_horizontal(self):
        return self.native.HorizontalScroll.Enabled

    def set_horizontal(self, value):
        if not value:
            self.native.HorizontalScroll.Value = 0

        self.native.AutoScroll = False
        self.native.HorizontalScroll.Enabled = value
        self.native.HorizontalScroll.Visible = value
        self.native.AutoScroll = True
        self.resize_content()

    def get_vertical(self):
        return self.native.VerticalScroll.Enabled

    def set_vertical(self, value):
        if not value:
            self.native.VerticalScroll.Value = 0

        self.native.AutoScroll = False
        self.native.VerticalScroll.Enabled = value
        self.native.VerticalScroll.Visible = value
        self.native.AutoScroll = True
        self.resize_content()

    def set_window(self, window):
        if self.interface.content:
            self.interface.content.window = window

    def get_vertical_position(self):
        return self.scale_out(self.native.VerticalScroll.Value)

    def get_horizontal_position(self):
        return self.scale_out(self.native.HorizontalScroll.Value)

    def get_max_vertical_position(self):
        return self.scale_out(self.native.VerticalScroll.Maximum)

    def get_max_horizontal_position(self):
        return self.scale_out(self.native.HorizontalScroll.Maximum)

    def set_position(self, horizontal_position, vertical_position):
        self.native.HorizontalScroll.Value = self.scale_in(horizontal_position)
        self.native.VerticalScroll.Value = self.scale_in(vertical_position)
