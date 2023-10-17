import pytest
from pytest import approx
from System import EventArgs, Object
from System.Drawing import Color, SystemColors
from System.Windows.Forms import MouseButtons, MouseEventArgs

from toga.colors import TRANSPARENT
from toga.style.pack import JUSTIFY, LEFT

from ..fonts import FontMixin
from ..probe import BaseProbe
from .properties import toga_color


class SimpleProbe(BaseProbe, FontMixin):
    fixed_height = None

    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
        self.widget = widget
        self.impl = widget._impl
        self.native = self.impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        assert self.widget._impl.container is container._impl.container
        assert self.native.Parent is not None
        assert Object.ReferenceEquals(
            self.native.Parent,
            container._impl.container.native_content,
        )

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.Parent is None

    def assert_alignment(self, expected):
        # Winforms doesn't have a "Justified" alignment; it falls back to LEFT
        actual = self.alignment
        if expected == JUSTIFY:
            assert actual == LEFT
        else:
            assert actual == expected

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
        if self.native.BackColor == Color.Transparent:
            return TRANSPARENT
        else:
            return toga_color(self.native.BackColor)

    @property
    def font(self):
        return self.native.Font

    @property
    def hidden(self):
        return not self.native.Visible

    @property
    def width(self):
        return round(self.native.Width / self.scale_factor)

    @property
    def height(self):
        return round(self.native.Height / self.scale_factor)

    def assert_width(self, min_width, max_width):
        assert (
            min_width <= self.width <= max_width
        ), f"Width ({self.width}) not in range ({min_width}, {max_width})"

    def assert_height(self, min_height, max_height):
        if self.fixed_height is not None:
            assert self.height == approx(self.fixed_height, rel=0.1)
        else:
            assert min_height <= self.height <= max_height

    @property
    def shrink_on_resize(self):
        return True

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.Parent is not None

        # size and position is as expected.
        assert (self.width, self.height) == approx(size, abs=1)
        assert (
            self.native.Left / self.scale_factor,
            self.native.Top / self.scale_factor,
        ) == approx(position, abs=1)

    async def press(self):
        self.native.OnClick(EventArgs.Empty)

    def mouse_event(self, x=0, y=0, **kwargs):
        kwargs = {**dict(button=MouseButtons.Left, clicks=1, delta=0), **kwargs}
        return MouseEventArgs(
            x=round(x * self.scale_factor), y=round(y * self.scale_factor), **kwargs
        )

    @property
    def is_hidden(self):
        return not self.native.Visible

    @property
    def has_focus(self):
        return self.native.ContainsFocus

    async def undo(self):
        pytest.skip("Undo not supported on this platform")

    async def redo(self):
        pytest.skip("Redo not supported on this platform")
