from io import BytesIO

import pytest
from PIL import Image

from toga_gtk.libs import Gdk, Gtk

from .base import SimpleProbe


class CanvasProbe(SimpleProbe):
    native_class = Gtk.DrawingArea

    def reference_variant(self, reference):
        if reference in {"write_text", "multiline_text"}:
            pytest.skip(
                "GTK canvas font handling isn't quite right: "
                "https://github.com/beeware/toga/pull/2029#issuecomment-1722619278"
            )
        else:
            return reference

    def get_image(self):
        return Image.open(BytesIO(self.impl.get_image_data()))

    def assert_image_size(self, image, width, height):
        assert image.width == width
        assert image.height == height

    async def mouse_press(self, x, y):
        event = Gdk.Event.new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.x = x
        event.y = y
        self.native.emit("button-press-event", event)

        event = Gdk.Event.new(Gdk.EventType.BUTTON_RELEASE)
        event.button = 1
        event.x = x
        event.y = y
        self.native.emit("button-release-event", event)

    async def mouse_activate(self, x, y):
        event = Gdk.Event.new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.x = x
        event.y = y
        self.native.emit("button-press-event", event)

        event = Gdk.Event.new(Gdk.EventType.BUTTON_RELEASE)
        event.button = 1
        event.x = x
        event.y = y
        self.native.emit("button-release-event", event)

        event = Gdk.Event.new(Gdk.EventType.DOUBLE_BUTTON_PRESS)
        event.button = 1
        event.x = x
        event.y = y
        self.native.emit("button-press-event", event)

        event = Gdk.Event.new(Gdk.EventType.BUTTON_RELEASE)
        event.button = 1
        event.x = x
        event.y = y
        self.native.emit("button-release-event", event)

    async def mouse_drag(self, x1, y1, x2, y2):
        event = Gdk.Event.new(Gdk.EventType.BUTTON_PRESS)
        event.button = 1
        event.x = x1
        event.y = y1
        self.native.emit("button-press-event", event)

        event = Gdk.Event.new(Gdk.EventType.MOTION_NOTIFY)
        event.button = 1
        event.state = Gdk.ModifierType.BUTTON1_MASK
        event.x = (x1 + x2) // 2
        event.y = (y1 + y2) // 2
        self.native.emit("motion-notify-event", event)

        event = Gdk.Event.new(Gdk.EventType.BUTTON_RELEASE)
        event.button = 1
        event.x = x2
        event.y = y2
        self.native.emit("button-release-event", event)

    async def alt_mouse_press(self, x, y):
        event = Gdk.Event.new(Gdk.EventType.BUTTON_PRESS)
        event.button = 3
        event.x = x
        event.y = y
        self.native.emit("button-press-event", event)

        event = Gdk.Event.new(Gdk.EventType.BUTTON_RELEASE)
        event.button = 3
        event.x = x
        event.y = y
        self.native.emit("button-release-event", event)

    async def alt_mouse_drag(self, x1, y1, x2, y2):
        event = Gdk.Event.new(Gdk.EventType.BUTTON_PRESS)
        event.button = 3
        event.x = x1
        event.y = y1
        self.native.emit("button-press-event", event)

        event = Gdk.Event.new(Gdk.EventType.MOTION_NOTIFY)
        event.state = Gdk.ModifierType.BUTTON3_MASK
        event.x = (x1 + x2) // 2
        event.y = (y1 + y2) // 2
        self.native.emit("motion-notify-event", event)

        event = Gdk.Event.new(Gdk.EventType.BUTTON_RELEASE)
        event.button = 3
        event.x = x2
        event.y = y2
        self.native.emit("button-release-event", event)