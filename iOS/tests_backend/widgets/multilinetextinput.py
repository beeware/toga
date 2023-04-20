from toga_iOS.libs import UITextView

from .base import SimpleProbe


class MultilineTextInputProbe(SimpleProbe):
    native_class = UITextView

    @property
    def readonly(self):
        return not self.native.isEditable()
