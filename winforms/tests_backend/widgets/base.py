from System import EventArgs, Object
from System.Drawing import SystemColors

from toga.colors import TRANSPARENT
from toga.style.pack import JUSTIFY, LEFT

from .properties import toga_color, toga_font


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

    def alignment_equivalent(self, actual, expected):
        # Winforms doesn't have a "Justified" alignment; it falls back to LEFT
        if expected == JUSTIFY:
            assert actual == LEFT
        else:
            assert actual == expected
        return True

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # TODO: Travertino/Pack doesn't force a layout refresh
        # when properties such as flex or width are altered.
        # For now, do a manual refresh.
        self.widget.window.content.refresh()

    @property
    def enabled(self):
        return self.native.Enabled

    @property
    def color(self):
        if self.native.ForeColor == SystemColors.WindowText:
            return None
        else:
            return toga_color(self.native.ForeColor)

    @property
    def background_color(self):
        if self.native.BackColor == SystemColors.Control:
            return TRANSPARENT
        else:
            return toga_color(self.native.BackColor)

    @property
    def font(self):
        return toga_font(self.native.Font)

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
