from ..container import Container
from ..libs import WinForms
from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = WinForms.ScrollableControl()
        self.native.AutoScroll = True

    def set_content(self, widget):
        if widget.native is None:
            self.inner_container = Container()
            self.inner_container.content = widget
        else:
            self.inner_container = widget

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
