from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = Gtk.ProgressBar

    @property
    def is_determinate(self):
        return self.widget._impl._max is not None

    @property
    def is_animating_indeterminate(self):
        # Cocoa doesn't require any explicit animation flags required
        return not self.is_determinate and self.widget._impl._running

    @property
    def value_ratio(self):
        return self.native.get_fraction()
