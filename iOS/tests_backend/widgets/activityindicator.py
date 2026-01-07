from toga_iOS.libs import UIActivityIndicatorView

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = UIActivityIndicatorView

    def assert_spinner_is_hidden(self, value):
        assert self.native.isHidden() == value
