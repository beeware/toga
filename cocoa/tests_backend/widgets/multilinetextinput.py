from toga_cocoa.libs import NSScrollView

from .base import SimpleProbe


class MultilineTextInputProbe(SimpleProbe):
    native_class = NSScrollView

    @property
    def enabled(self):
        return self.native.documentView.isEditable()
