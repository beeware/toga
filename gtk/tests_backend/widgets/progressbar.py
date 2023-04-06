from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = Gtk.ProgressBar

    @property
    def is_determinate(self):
        return self.widget._impl._max is not None

    @property
    def is_animating_indeterminate(self):
        return not self.is_determinate and self.widget._impl._running

    @property
    def position(self):
        return self.native.get_fraction()
