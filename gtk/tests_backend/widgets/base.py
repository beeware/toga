import asyncio
import warnings

from pytest import skip

from toga_gtk.libs import Gio, Gtk

from .properties import toga_color, toga_font


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

        # Check if GTK UI animations are enabled.
        settings = Gio.Settings(schema="org.gnome.desktop.interface")
        if settings.get_boolean("enable-animations"):
            warnings.warn(
                "GTK UI animations are enabled; any tests failures are likely "
                "caused by this. Run `gsettings set org.gnome.desktop.interface "
                "enable-animations false` to disable animations.",
                RuntimeWarning,
            )

    def assert_container(self, container):
        container_native = container._impl.container
        for control in container_native.get_children():
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    def assert_alignment_equivalent(self, actual, expected):
        assert actual == expected

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        while self.impl.container.needs_redraw or Gtk.events_pending():
            Gtk.main_iteration_do(blocking=False)

        # If we're running slow, wait for a second
        if self.widget.app.run_slow:
            await asyncio.sleep(1)

    @property
    def enabled(self):
        skip("enabled probe not implemented")

    @property
    def hidden(self):
        skip("hidden probe not implemented")

    @property
    def width(self):
        return self.native.get_allocation().width

    @property
    def height(self):
        return self.native.get_allocation().height

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
