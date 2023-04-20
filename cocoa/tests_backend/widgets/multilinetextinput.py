from toga_cocoa.libs import NSScrollView

from .base import SimpleProbe


class MultilineTextInputProbe(SimpleProbe):
    native_class = NSScrollView

    @property
    def readonly(self):
        return not self.native.documentView.isEditable()
