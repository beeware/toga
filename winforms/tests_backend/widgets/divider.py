import System.Windows.Forms

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def enabled(self):
        # A Divider is always enabled.
        return True
