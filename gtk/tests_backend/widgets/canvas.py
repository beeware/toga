import os
from io import BytesIO

import pytest
from PIL import Image

from toga_gtk.libs import GTK_VERSION, IS_WAYLAND, Gdk, Gtk

from .base import SimpleProbe


class CanvasProbe(SimpleProbe):
    native_class = Gtk.DrawingArea

    def reference_variant(self, reference):
        if reference == "multiline_text":
            if IS_WAYLAND:
                return f"{reference}-gtk-wayland"
            else:
                return f"{reference}-gtk-x11"
        elif reference == "write_text":
            if GTK_VERSION < (4, 0, 0) or os.environ.get("WAYLAND_DISPLAY") == "toga":
                return f"{reference}-gtk"
            else:
                # Ubuntu 24.04 renders kerning etc. slightly
                # differently locally compared to CI, only on GTK4.
                return f"{reference}-gtk4-local"
        else:
            return reference

    def get_image(self):
        return Image.open(BytesIO(self.impl.get_image_data()))

    if GTK_VERSION < (4, 0, 0):

        def _emit_event(self, event_type, x, y, button=1, state=0, emit_name=None):
            event = Gdk.Event.new(event_type)
            event.button = button
            event.x = x
            event.y = y
            if event_type == Gdk.EventType.MOTION_NOTIFY:
                state = state | getattr(Gdk.ModifierType, f"BUTTON{button}_MASK")
            event.state = state

            self.native.emit(
                emit_name or event_type.name.lower().replace("_", "-") + "-event", event
            )

    else:
        # There is not a public mechanism to send such events in GTK4 directly;
        # therefore, get the controller to emit signals, as well as assert that
        # they'll be looking for the correct button presses in production.
        def _controller_emit(self, event_name, times, x, y, button=1):
            if event_name == "motion":
                self.impl.motion_controller.emit("motion", x, y)
            else:
                if button == 1:
                    controller = self.impl.main_gesture
                elif button == 3:
                    controller = self.impl.alt_gesture
                else:
                    pytest.fail("Unsupported press for controller")
                assert controller.get_button() == button

                controller.emit(event_name, times, x, y)

    async def mouse_press(self, x, y):
        if GTK_VERSION < (4, 0, 0):
            self._emit_event(Gdk.EventType.BUTTON_PRESS, x, y, button=1)
            self._emit_event(Gdk.EventType.BUTTON_RELEASE, x, y, button=1)
        else:
            self._controller_emit("pressed", 1, x, y, button=1)
            self._controller_emit("released", 1, x, y, button=1)

    async def mouse_activate(self, x, y):
        if GTK_VERSION < (4, 0, 0):
            self._emit_event(Gdk.EventType.BUTTON_PRESS, x, y, button=1)
            self._emit_event(Gdk.EventType.BUTTON_RELEASE, x, y, button=1)
            self._emit_event(
                Gdk.EventType.DOUBLE_BUTTON_PRESS,
                x,
                y,
                button=1,
                emit_name="button-press-event",
            )
            self._emit_event(Gdk.EventType.BUTTON_RELEASE, x, y, button=1)
        else:
            self._controller_emit("pressed", 1, x, y, button=1)
            self._controller_emit("released", 1, x, y, button=1)
            self._controller_emit("pressed", 2, x, y, button=1)
            self._controller_emit("released", 2, x, y, button=1)

    async def mouse_drag(self, x1, y1, x2, y2):
        if GTK_VERSION < (4, 0, 0):
            self._emit_event(Gdk.EventType.BUTTON_PRESS, x1, y1, button=1)
            self._emit_event(
                Gdk.EventType.MOTION_NOTIFY,
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                button=1,
                state=Gdk.ModifierType.MOD2_MASK,
            )
            self._emit_event(Gdk.EventType.BUTTON_RELEASE, x2, y2, button=1)
        else:
            self._controller_emit("pressed", 1, x1, y1, button=1)
            self._controller_emit("motion", 1, (x1 + x2) // 2, (y1 + y2) // 2, button=1)
            self._controller_emit("released", 1, x2, y2, button=1)

    async def alt_mouse_press(self, x, y):
        if GTK_VERSION < (4, 0, 0):
            self._emit_event(Gdk.EventType.BUTTON_PRESS, x, y, button=3)
            self._emit_event(Gdk.EventType.BUTTON_RELEASE, x, y, button=3)
        else:
            self._controller_emit("pressed", 1, x, y, button=3)
            self._controller_emit("released", 1, x, y, button=3)

    async def alt_mouse_drag(self, x1, y1, x2, y2):
        if GTK_VERSION < (4, 0, 0):
            self._emit_event(Gdk.EventType.BUTTON_PRESS, x1, y1, button=3)
            self._emit_event(
                Gdk.EventType.MOTION_NOTIFY,
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                button=3,
                state=Gdk.ModifierType.MOD2_MASK,
            )
            self._emit_event(Gdk.EventType.BUTTON_RELEASE, x2, y2, button=3)
        else:
            self._controller_emit("pressed", 1, x1, y1, button=3)
            self._controller_emit("motion", 1, (x1 + x2) // 2, (y1 + y2) // 2, button=3)
            self._controller_emit("released", 1, x2, y2, button=3)
