import System.Windows.Forms as WinForms
from System.Drawing import Size

from .widgets.base import Scalable


class Container(Scalable):
    def __init__(self, native_parent):
        self.init_scale(native_parent)
        self.native_parent = native_parent
        self.native_width = self.native_height = 0
        self.content = None

        self.native_content = WinForms.Panel()
        native_parent.Controls.Add(self.native_content)

    @property
    def width(self):
        return self.scale_out(self.native_width)

    @property
    def height(self):
        return self.scale_out(self.native_height)

    def set_content(self, widget):
        self.clear_content()
        if widget:
            widget.container = self
            self.content = widget

    def clear_content(self):
        if self.content:
            self.content.container = None
            self.content = None

    def resize_content(self, width, height, *, force_refresh=False):
        if (self.native_width, self.native_height) != (width, height):
            self.native_width, self.native_height = (width, height)
            force_refresh = True

        if force_refresh and self.content:
            self.content.interface.refresh()

    def refreshed(self):
        layout = self.content.interface.layout
        self.apply_layout(layout.width, layout.height)

    def apply_layout(self, layout_width, layout_height):
        self.native_content.Size = Size(
            self.scale_in(max(self.width, layout_width)),
            self.scale_in(max(self.height, layout_height)),
        )

    def add_content(self, widget):
        # The default is to add new controls to the back of the Z-order.
        self.native_content.Controls.Add(widget.native)
        widget.native.BringToFront()

    def remove_content(self, widget):
        self.native_content.Controls.Remove(widget.native)
