from toga_gtk.libs import GTK_VERSION, Gdk, Gtk

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = Gtk.Scale

    @property
    def position(self):
        assert self.native.get_draw_value() is False
        return (self.native.get_value() - self._min) / (self._max - self._min)

    async def change(self, position):
        self.native.emit(
            "change-value",
            Gtk.ScrollType.JUMP,
            self._min + (position * (self._max - self._min)),
        )

    @property
    def tick_count(self):
        # There is no get_marks method, nor any other way of getting that information as
        # far as I can see.
        raise NotImplementedError()

    @property
    def _min(self):
        return self.impl.adj.get_lower()

    @property
    def _max(self):
        return self.impl.adj.get_upper()

    async def press(self):
        if GTK_VERSION < (4, 0, 0):
            self.native.emit("button-press-event", Gdk.Event())
        else:
            self.impl.click_controller.emit("pressed", 1, 0.0, 0.0)

    async def release(self):
        if GTK_VERSION < (4, 0, 0):
            self.native.emit("button-release-event", Gdk.Event())
        else:
            self.impl.click_controller.emit("released", 1, 0.0, 0.0)
