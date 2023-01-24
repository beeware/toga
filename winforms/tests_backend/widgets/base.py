from System import EventArgs, Object

from .properties import toga_color


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        container_native = container._impl.native
        for control in container_native.Controls:
            if Object.ReferenceEquals(control, self.native):
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Refresh the layout
        self.widget.window.content.refresh()

    @property
    def enabled(self):
        return self.native.Enabled

    @property
    def background_color(self):
        return toga_color(self.native.BackColor)

    @property
    def color(self):
        return toga_color(self.native.ForeColor)

    @property
    def hidden(self):
        return not self.native.Visible

    @property
    def width(self):
        return self.native.Width

    @property
    def height(self):
        return self.native.Height

    def press(self):
        self.native.OnClick(EventArgs.Empty)
