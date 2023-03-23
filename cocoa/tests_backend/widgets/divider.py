from toga_cocoa.libs import NSBox

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = NSBox

    @property
    def direction(self):
        # Cocoa doesn't have a native concept of divider direction;
        # use the impl's proxy representation.
        return self.widget._impl._direction
