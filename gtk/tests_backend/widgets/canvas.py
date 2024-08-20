from io import BytesIO

from PIL import Image

from toga_gtk.libs import IS_WAYLAND, Gdk, Gtk

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
            return f"{reference}-gtk"
        else:
            return reference

    def get_image(self):
        return Image.open(BytesIO(self.impl.get_image_data()))

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
