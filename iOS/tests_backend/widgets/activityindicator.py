from toga_iOS.libs import UIActivityIndicatorView

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = UIActivityIndicatorView

    @property
    def is_hidden(self):
        return self.native.isHidden()
