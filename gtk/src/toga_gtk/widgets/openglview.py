from travertino.size import at_least

from toga.widgets.openglview import LEFT, MIDDLE, RIGHT
from toga_gtk.libs import GTK_VERSION, Gdk, Gtk

from .base import Widget

BUTTONS = [LEFT, MIDDLE, RIGHT]


class OpenGLView(Widget):
    def create(self):
        self.native = Gtk.GLArea()
        self.native.connect("realize", self.gtk_realize)
        self.native.connect("render", self.gtk_render)

        self.buttons = set()
        self.position = None

        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.connect("button-press-event", self.gtk_button_press)
            self.native.connect("button-release-event", self.gtk_button_release)
            self.native.connect("motion-notify-event", self.gtk_motion_notify)
            self.native.set_events(
                Gdk.EventMask.BUTTON_PRESS_MASK
                | Gdk.EventMask.BUTTON_RELEASE_MASK
                | Gdk.EventMask.BUTTON_MOTION_MASK
            )
        else:  # pragma: no-cover-if-gtk3
            # Currently unsure of how best to integrate GTK 4 gestures with mouse state
            pass

    def gtk_realize(self, native):
        """Initialize the OpenGL context."""
        ctx = self.native.get_context()
        ctx.make_current()
        self.interface.renderer.on_init(self.interface)

    def gtk_render(self, native, context):
        """Render to the OpenGL context."""
        self.interface.renderer.on_render(
            self.interface,
            size=self._size(),
            buttons=self.buttons,
            position=self.position,
        )
        return True

    if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4

        def gtk_button_press(self, obj, event):
            self.buttons.add(BUTTONS[event.button])
            self.position = (event.x, event.y)

        def gtk_button_release(self, obj, event):
            self.buttons.discard(BUTTONS[event.button])
            self.position = (event.x, event.y)

        def gtk_motion_notify(self, obj, event):
            self.position = (event.x, event.y)

    def _size(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            width = self.native.get_allocation().width
            height = self.native.get_allocation().height
        else:  # pragma: no-cover-if-gtk3
            width = self.native.compute_bounds(self.native)[1].get_width()
            height = self.native.compute_bounds(self.native)[1].get_height()
        return width, height

    def redraw(self):
        self.native.queue_draw()

    def rehint(self):
        width = self.interface._MIN_WIDTH
        height = self.interface._MIN_HEIGHT
        self.interface.intrinsic.height = at_least(width)
        self.interface.intrinsic.width = at_least(height)
