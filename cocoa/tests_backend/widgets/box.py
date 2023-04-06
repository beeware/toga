from toga_cocoa.libs import NSView

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = NSView
