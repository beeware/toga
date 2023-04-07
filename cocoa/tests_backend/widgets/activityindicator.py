from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = NSProgressIndicator
