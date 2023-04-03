import System.Windows.Forms

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = System.Windows.Forms.Panel

    @property
    def enabled(self):
        # A box is always enabled.
        return True
