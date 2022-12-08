from toga_cocoa.libs import NSTextField

from .base import SimpleProbe


class LabelProbe(SimpleProbe):
    native_class = NSTextField

    @property
    def text(self):
        return self.native.stringValue
