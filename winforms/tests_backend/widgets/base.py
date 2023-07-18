from pytest import approx
from System import EventArgs, Object
from System.Drawing import SystemColors
from System.Windows.Forms import SendKeys

from toga.colors import TRANSPARENT
from toga.style.pack import JUSTIFY, LEFT

from ..probe import BaseProbe
from .properties import toga_color, toga_font

KEY_CODES = {
    f"<{name}>": f"{{{name.upper()}}}"
    for name in ["esc", "up", "down", "left", "right"]
}
KEY_CODES.update(
    {
        "\n": "{ENTER}",
    }
)


class SimpleProbe(BaseProbe):
    fixed_height = None

    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
        self.widget = widget
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)
        self.scale_factor = self.native.CreateGraphics().DpiX / 96

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
            assert self.height == approx(self.fixed_height, rel=0.2)
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

    async def type_character(self, char):
        try:
            key_code = KEY_CODES[char]
        except KeyError:
            assert len(char) == 1, char
            key_code = char

        SendKeys.SendWait(key_code)

    @property
    def is_hidden(self):
        return not self.native.Visible

    @property
    def has_focus(self):
        return self.native.ContainsFocus
