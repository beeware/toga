from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = NSProgressIndicator

    @property
    def is_hidden(self):
        return self.native.isHidden()
