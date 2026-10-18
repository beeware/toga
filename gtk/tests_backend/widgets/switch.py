from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe
from .properties import toga_color, toga_font


class SwitchProbe(SimpleProbe):
    native_class = Gtk.Box

    def __init__(self, widget):
        super().__init__(widget)
        self.native_label = widget._impl.native_label
        self.native_switch = widget._impl.native_switch
        assert self.native_label.get_parent() == self.native
        assert self.native_switch.get_parent() == self.native

    @property
    def enabled(self):
        return self.native_label.get_sensitive() and self.native_switch.get_sensitive()

    @property
    def text(self):
        return self.native_label.get_label()

    @property
    def color(self):
        if GTK_VERSION < (4, 0, 0):
            sc = self.native_label.get_style_context()
            return toga_color(sc.get_property("color", sc.get_state()))
        else:
            style_provider = self.impl.style_providers.get(
                ("color", id(self.native_label))
            )
            style_value = (
                style_provider.to_string().split(": ")[1].split(";")[0]
                if style_provider
                else None
            )
            return toga_color(style_value) if style_value else None

    @property
    def font(self):
        if GTK_VERSION < (4, 0, 0):
            sc = self.native_label.get_style_context()
            return sc.get_property("font", sc.get_state())
        else:
            style_provider = self.impl.style_providers.get(
                ("font", id(self.native_label))
            )
            return toga_font(style_provider.to_string()) if style_provider else None

    def assert_width(self, min_width, max_width):
        super().assert_width(min_width, max_width)

        # Also check the width of the two inner components
        if GTK_VERSION < (4, 0, 0):
            label_width = self.native_label.get_allocation().width
            switch_width = self.native_switch.get_allocation().width
        else:
            label_width = self.native_label.compute_bounds(self.native_label)[
                1
            ].get_width()
            switch_width = self.native_switch.compute_bounds(self.native_switch)[
                1
            ].get_width()

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

        if GTK_VERSION < (4, 0, 0):
            label_height = self.native_label.get_allocation().height
            switch_height = self.native_switch.get_allocation().height
        else:
            label_height = self.native_label.compute_bounds(self.native_label)[
                1
            ].get_height()
            switch_height = self.native_switch.compute_bounds(self.native_switch)[
                1
            ].get_height()
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
