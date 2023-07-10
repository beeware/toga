from toga_winforms.libs import Size, WinForms


class BaseContainer:
    def init_container(self, native_parent):
        self.width = self.height = 0
        self.baseline_dpi = 96
        self.dpi = native_parent.CreateGraphics().DpiX


class MinimumContainer(BaseContainer):
    def __init__(self, native_parent):
        self.init_container(native_parent)

    def refreshed(self):
        pass


class Container(BaseContainer):
    def init_container(self, native_parent):
        super().init_container(native_parent)
        self.native_content = WinForms.Panel()
        native_parent.Controls.Add(self.native_content)

    def set_content(self, widget):
        self.clear_content()
        if widget:
            widget.container = self

    def clear_content(self):
        if self.interface.content:
            self.interface.content._impl.container = None

    def resize_content(self, width, height):
        if (self.width, self.height) != (width, height):
            self.width, self.height = (width, height)
            if self.interface.content:
                self.interface.content.refresh()

    def refreshed(self):
        layout = self.interface.content.layout
        self.native_content.Size = Size(
            max(self.width, layout.width),
            max(self.height, layout.height),
        )

    def add_content(self, widget):
        # The default appears to be to add new controls to the back of the Z-order.
        self.native_content.Controls.Add(widget.native)
        widget.native.BringToFront()

    def remove_content(self, widget):
        self.native_content.Controls.Remove(widget.native)
