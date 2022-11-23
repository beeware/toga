from System import EventArgs, Object

from toga.colors import rgba


class SimpleProbe:
    """Probe for a Toga widget that generates a single native widget."""

    def __init__(self, main_box, widget):
        native_box = main_box._impl.native
        assert native_box.Controls.Count == 1
        self.native = native_box.Controls[0]
        assert isinstance(self.native, self.native_class)

        # Although this isn't part of the public API, we often point users at it to do
        # things that Toga itself doesn't support.
        assert Object.ReferenceEquals(widget._impl.native, self.native)

    @property
    def enabled(self):
        return self.native.Enabled

    @property
    def color(self):
        c = self.native.ForeColor
        return rgba(c.R, c.G, c.B, c.A / 255)

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
