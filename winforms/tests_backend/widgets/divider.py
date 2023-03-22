import System.Windows.Forms

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def direction(self):
        # Winforms doesn't have a native concept of divider direction;
        # use the impl's proxy representation.
        return self.widget._impl._direction
