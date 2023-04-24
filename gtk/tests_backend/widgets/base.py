import asyncio

import pytest

from toga_gtk.libs import Gtk

from .properties import toga_color, toga_font


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

        # Ensure that the theme isn't using animations for the widget.
        settings = Gtk.Settings.get_for_screen(self.native.get_screen())
        settings.set_property("gtk-enable-animations", False)

    def assert_container(self, container):
        container_native = container._impl.container
        for control in container_native.get_children():
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.get_parent() is None

    def assert_alignment(self, expected):
        assert self.alignment == expected

    def assert_font_family(self, expected):
        assert self.font.family == expected

    async def redraw(self, message=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        while self.impl.container.needs_redraw or Gtk.events_pending():
            Gtk.main_iteration_do(blocking=False)

        # If we're running slow, wait for a second
        if self.widget.app.run_slow:
            if not (message is None):
                if message == "":
                    message = "Waiting for redraw"
                print("\n%s" % message)
            await asyncio.sleep(1)

    @property
    def enabled(self):
        return self.native.get_sensitive()

    @property
    def width(self):
        return self.native.get_allocation().width

    @property
    def height(self):
        return self.native.get_allocation().height

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.get_parent() is not None

        # Measurements are relative to the container as an origin.
        origin = self.widget._impl.container.get_allocation()

        # size and position is as expected.
        assert (
            self.native.get_allocation().width,
            self.native.get_allocation().height,
        ) == size
        assert (
            self.native.get_allocation().x - origin.x,
            self.native.get_allocation().y - origin.y,
        ) == position

    def assert_width(self, min_width, max_width):
        assert (
            min_width <= self.width <= max_width
        ), f"Width ({self.width}) not in range ({min_width}, {max_width})"

    def assert_height(self, min_height, max_height):
        assert (
            min_height <= self.height <= max_height
        ), f"Height ({self.height}) not in range ({min_height}, {max_height})"

    @property
    def color(self):
        sc = self.native.get_style_context()
        return toga_color(sc.get_property("color", sc.get_state()))

    @property
    def background_color(self):
        sc = self.native.get_style_context()
        return toga_color(sc.get_property("background-color", sc.get_state()))

    @property
    def font(self):
        sc = self.native.get_style_context()
        return toga_font(sc.get_property("font", sc.get_state()))

    @property
    def is_hidden(self):
        return not self.native.get_visible()

    @property
    def has_focus(self):
        # FIXME: This works when running standalone, but fails under CI.
        # I *think* this is because CI is using xvfb.
        # return self.native.has_focus()
        pytest.skip("Focus changes don't work on GTK inside XVFB")
