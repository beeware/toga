import pytest
from pytest import approx
from System import EventArgs, Object
from System.Drawing import SystemColors
from System.Windows.Forms import MouseButtons, MouseEventArgs

from toga.style.pack import JUSTIFY, LEFT

from ..probe import BaseProbe
from .properties import toga_color


class SimpleProbe(BaseProbe):
    def __init__(self, widget):
        self.app = widget.app
        self.widget = widget
        self.impl = widget._impl
        super().__init__(self.impl.native)
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

    def assert_text_align(self, expected):
        # Winforms doesn't have a "Justified" text alignment; it falls back to LEFT
        actual = self.text_align
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
        return (
            toga_color(self.native.BackColor),
            toga_color(self.widget.parent._impl.native.BackColor),
            (
                # self.impl.interface.style.background_color can be None or TRANSPARENT
                # and so there will be no alpha value on them. In such cases return 0
                # as the original alpha value.
                getattr(self.widget.style.background_color, "a", 0)
            ),
        )

    @property
    def hidden(self):
        return not self.native.Visible

    @property
    def shrink_on_resize(self):
        return True

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.Parent is not None

        # size and position is as expected.
        assert (self.width, self.height) == approx(size, abs=1)
        assert (self.x, self.y) == approx(position, abs=1)

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
