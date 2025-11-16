import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe
from .properties import toga_color, toga_font


class SwitchProbe(SimpleProbe):
    native_class = Gtk.Box

    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("GTK4 doesn't support switches yet")

    def __init__(self, widget):
        super().__init__(widget)
        self.native_label = widget._impl.native_label
        self.native_switch = widget._impl.native_switch

    @property
    def enabled(self):
        return self.native_label.get_sensitive() and self.native_switch.get_sensitive()

    @property
    def text(self):
        return self.native_label.get_label()

    @property
    def color(self):
        style_provider = self.impl.style_providers.get(("color", id(self.native_label)))
        color_value = (
            style_provider.to_string().split(": ")[1].split(";")[0]
            if style_provider
            else None
        )
        return toga_color(color_value) if color_value else None

    @property
    def font(self):
        style_provider = self.impl.style_providers.get(("font", id(self.native_label)))
        font_value = style_provider.to_string() if style_provider else None
        return toga_font(font_value) if font_value else None

    def assert_width(self, min_width, max_width):
        super().assert_width(min_width, max_width)

        # Also check the width of the two inner components
        label_width = self.native_label.get_allocation().width
        switch_width = self.native_switch.get_allocation().width

        # The switch should be ~50px wide.
        MAX_SWITCH_WIDTH = 60

        assert (
            (min_width - MAX_SWITCH_WIDTH)
            <= label_width
            <= (max_width - MAX_SWITCH_WIDTH)
        ), (
            f"Label width ({label_width}) not in range "
            f"({min_width - MAX_SWITCH_WIDTH}, {max_width - MAX_SWITCH_WIDTH})"
        )
        assert 0 <= switch_width <= MAX_SWITCH_WIDTH, (
            f"Switch width ({switch_width}) not in range (0-60)"
        )

    def assert_height(self, min_height, max_height):
        super().assert_height(min_height, max_height)

        label_height = self.native_label.get_allocation().height
        switch_height = self.native_switch.get_allocation().height
        assert min_height <= label_height <= max_height, (
            f"Label height ({label_height}) not in range ({min_height}, {max_height})"
        )
        assert min_height <= switch_height <= max_height, (
            f"Switch height ({switch_height}) not in range ({min_height}, {max_height})"
        )

    async def press(self):
        # This isn't really a "click" - it's just changing the value.
        # However, Gtk doesn't seem to have a way to send a click to a switch,
        # and the underlying event on Gtk *is* a value change event.
        self.native_switch.set_active(not self.native_switch.get_active())
