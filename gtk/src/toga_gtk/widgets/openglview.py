from travertino.size import at_least

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import Widget


class OpenGLView(Widget):
    def create(self):
        self.native = Gtk.GLArea()
        self.native.connect("realize", self.gtk_realize)
        self.native.connect("render", self.gtk_render)

    def gtk_realize(self, native):
        """Initialize the OpenGL context."""
        ctx = self.native.get_context()
        ctx.make_current()
        self.interface.renderer.on_init(self.interface)

    def gtk_render(self, native, context):
        """Render to the OpenGL context."""
        self.interface.renderer.on_render(self.interface, size=self._size())
        return True

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
