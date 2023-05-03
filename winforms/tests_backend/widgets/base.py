import asyncio

from System import EventArgs, Object
from System.Drawing import FontFamily, SystemColors, SystemFonts

from toga.colors import TRANSPARENT
from toga.fonts import (
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MONOSPACE,
    NORMAL,
    SANS_SERIF,
    SERIF,
    SYSTEM,
)
from toga.style.pack import JUSTIFY, LEFT

from .properties import toga_color, toga_font


class SimpleProbe:
    FONT_WEIGHTS = [NORMAL, BOLD]
    FONT_STYLES = [NORMAL, ITALIC]
    FONT_VARIANTS = [NORMAL]

    def __init__(self, widget):
        self.widget = widget
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)
        self.scale_factor = self.native.CreateGraphics().DpiX / 96

    def assert_container(self, container):
        container_native = container._impl.native
        for control in container_native.Controls:
            if Object.ReferenceEquals(control, self.native):
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

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

    def assert_font_family(self, expected):
        assert self.font.family == {
            CURSIVE: "Comic Sans MS",
            FANTASY: "Impact",
            MONOSPACE: FontFamily.GenericMonospace.Name,
            SANS_SERIF: FontFamily.GenericSansSerif.Name,
            SERIF: FontFamily.GenericSerif.Name,
            SYSTEM: SystemFonts.DefaultFont.FontFamily.Name,
        }.get(expected, expected)

    async def redraw(self, message=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Winforms style changes always take effect immediately.

        # If we're running slow, wait for a second
        if self.widget.app.run_slow:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(1)

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
        return self.native.Width / self.scale_factor

    @property
    def height(self):
        return self.native.Height / self.scale_factor

    def assert_width(self, min_width, max_width):
        assert (
            min_width <= self.width <= max_width
        ), f"Width ({self.width}) not in range ({min_width}, {max_width})"

    def assert_height(self, min_height, max_height):
        assert (
            min_height <= self.height <= max_height
        ), f"Height ({self.height}) not in range ({min_height}, {max_height})"

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.Parent is not None

        # size and position is as expected.
        assert (self.native.Width, self.native.Height) == size
        assert (
            self.native.Left,
            self.native.Top - self.widget._impl.container.vertical_shift,
        ) == position

    async def press(self):
        self.native.OnClick(EventArgs.Empty)

    @property
    def is_hidden(self):
        return not self.native.Visible

    @property
    def has_focus(self):
        return self.native.ContainsFocus
