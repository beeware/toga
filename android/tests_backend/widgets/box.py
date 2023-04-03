from java import jclass

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = jclass("android.widget.RelativeLayout")

    @property
    def enabled(self):
        # A box is always enabled.
        return True
