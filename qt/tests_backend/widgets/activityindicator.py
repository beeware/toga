from PySide6.QtQuickWidgets import QQuickWidget

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = QQuickWidget

    def assert_spinner_is_hidden(self, value):
        assert (not self.native.isVisible()) == value
