import asyncio
from threading import Event

import pytest

from toga_gtk.libs import Gdk, Gtk

from ..fonts import FontMixin
from ..probe import BaseProbe
from .properties import toga_color


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

    def repaint_needed(self):
        return self.impl.container.needs_redraw or super().repaint_needed()

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
    def shrink_on_resize(self):
        return True

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
        return sc.get_property("font", sc.get_state())

    @property
    def is_hidden(self):
        return not self.native.get_visible()

    @property
    def has_focus(self):
        return self.native.has_focus()

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
        # caused by typing a character doesn't fully propagate. A
        # short delay fixes this.
        await asyncio.sleep(0.04)

    async def undo(self):
        pytest.skip("Undo not supported on this platform")

    async def redo(self):
        pytest.skip("Redo not supported on this platform")
