import asyncio
from threading import Event

import pytest

from toga_gtk.libs import Gdk, Gtk

from ..fonts import FontMixin
from ..probe import BaseProbe
from .properties import toga_color, toga_font


class SimpleProbe(BaseProbe, FontMixin):
    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

        # Set the target for keypress events
        self._keypress_target = self.native

        # Ensure that the theme isn't using animations for the widget.
        settings = Gtk.Settings.get_for_display(self.native.get_display())
        settings.set_property("gtk-enable-animations", False)

    def assert_container(self, container):
        container_native = container._impl.container

        control = container_native.get_last_child()
        while control is not None:
            if control == self.native:
                break
            control = control.get_prev_sibling()
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.get_parent() is None

    def assert_alignment(self, expected):
        assert self.alignment == expected

    def repaint_needed(self):
        return self.impl.container.needs_redraw or super().repaint_needed()

    @property
    def enabled(self):
        return self.native.get_sensitive()

    @property
    def width(self):
        return self.native.compute_bounds(self.native)[1].get_width()

    @property
    def height(self):
        return self.native.compute_bounds(self.native)[1].get_height()

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.impl.container is not None
        assert self.native.get_parent() is not None

        # Measurements are relative to the container as an origin coordinate.
        # size and position is as expected.
        if self.is_hidden:
            # NOTE: The widget has no size when it is hidden, so, to make sure the
            # layout is not changed, we only need to check the layout of the widget
            # siblings by ensuring that the position of the visible widgets are not
            # within the hidden widget's boundaries.
            siblings = [sibling._impl.native for sibling in self.widget.parent.children]
            for sibling in siblings:
                sibling_origin = sibling.compute_bounds(self.impl.container)[1].origin
                if sibling.get_visible():
                    assert sibling_origin.x >= size[0] or sibling_origin.y >= size[1]
        else:
            assert (
                self.width,
                self.height,
            ) == size
            assert (
                self.native.compute_bounds(self.impl.container)[1].origin.x,
                self.native.compute_bounds(self.impl.container)[1].origin.y,
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
    def shrink_on_resize(self):
        return True

    @property
    def color(self):
        sp = self.impl.style_providers.get(("color", id(self.native)))
        style_value = sp.to_string().split(": ")[1].split(";")[0] if sp else None
        return toga_color(style_value) if style_value else None

    @property
    def background_color(self):
        sp = self.impl.style_providers.get(("background_color", id(self.native)))
        style_value = sp.to_string().split(": ")[1].split(";")[0] if sp else None
        return toga_color(style_value) if style_value else None

    @property
    def font(self):
        sp = self.impl.style_providers.get(("font", id(self.native)))
        font_value = sp.to_string() if sp else None
        return toga_font(font_value) if font_value else None

    @property
    def is_hidden(self):
        return not self.native.get_visible()

    @property
    def has_focus(self):
        root = self.native.get_root()
        focus_widget = root.get_focus()
        if focus_widget:
            if focus_widget == self.native:
                return self.native.has_focus()
            else:
                return focus_widget.is_ancestor(self.native)
        else:
            return False

    async def type_character(self, char):
        # Construct a GDK KeyPress event.
        keyval = getattr(
            Gdk,
            f"KEY_{char}",
            {
                " ": Gdk.KEY_space,
                "-": Gdk.KEY_minus,
                ".": Gdk.KEY_period,
                "\n": Gdk.KEY_Return,
                "<esc>": Gdk.KEY_Escape,
            }.get(char, Gdk.KEY_question),
        )

        event = Gdk.Event.new(Gdk.EventType.KEY_PRESS)
        event.window = self.widget.window._impl.native.get_window()
        event.time = Gtk.get_current_event_time()
        event.keyval = keyval
        event.length = 1
        event.string = char
        # event.group =
        # event.hardware_keycode =
        event.is_modifier = 0

        # Mock the event coming from the keyboard
        device = Gdk.Display.get_default().get_default_seat().get_keyboard()
        event.set_device(device)

        # There might be more than one event loop iteration before the key
        # event is fully handled; and there may be iterations of the event loop
        # where there are no pending events. However, we need to know for
        # certain that the key event has been handled.
        #
        # Set up a temporary handler to listen for events being processed.
        # When the key is pressed, use a threading.Event to signal that
        # we can continue.
        handled = Event()

        def event_handled(widget, e):
            if e.type == Gdk.EventType.KEY_PRESS and e.keyval == event.keyval:
                handled.set()

        handler_id = self._keypress_target.connect("event-after", event_handled)

        # Inject the event
        Gtk.main_do_event(event)

        # Run the event loop until the keypress has been handled.
        while not handled.is_set():
            Gtk.main_iteration_do(blocking=False)

        # Remove the temporary handler
        self._keypress_target.disconnect(handler_id)

        # GTK has an intermittent failure because on_change handler
        # caused by typing a character doesn't fully propegate. A
        # short delay fixes this.
        await asyncio.sleep(0.04)

    async def undo(self):
        pytest.skip("Undo not supported on this platform")

    async def redo(self):
        pytest.skip("Redo not supported on this platform")
