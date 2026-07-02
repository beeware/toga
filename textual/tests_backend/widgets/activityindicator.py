from textual.widgets import LoadingIndicator as TextualLoadingIndicator

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = TextualLoadingIndicator
    _size = 24

    @property
    def width(self):
        return self._size

    @property
    def height(self):
        return self._size

    def assert_spinner_is_hidden(self, value):
        assert (not self.native.visible) == value
