from toga_iOS.libs import UIView

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = UIView

    @property
    def enabled(self):
        # A Box is always enabled.
        return True
