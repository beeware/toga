from toga_gtk.libs import Gtk

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = Gtk.Scale

    @property
    def position(self):
        return (self.native.get_value() - self._min) / (self._max - self._min)

    def change(self, position):
        self.native.set_value(self._min + round(position * (self._max - self._min)))

    @property
    def _min(self):
        return self.impl.adj.get_lower()

    @property
    def _max(self):
        return self.impl.adj.get_upper()
