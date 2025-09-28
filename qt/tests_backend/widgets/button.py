from PySide6.QtWidgets import QPushButton

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = QPushButton

    @property
    def text(self):
        # Normalize the zero width space to the empty string.
        if self.native.text() == "\u200b":
            return ""
        return self.native.text()

    def assert_no_icon(self):
        assert self.native.icon().isNull()

    def assert_icon_size(self):
        # Icons sizes in Qt are handled by the system theme;
        # no assertion is needed here.
        pass

    def assert_taller_than(self, initial_height):
        # Icons sizes in Qt are handled by the system theme;
        # no assertion is needed here, as whether the icon is
        # smaller or larger than text height does not matter.
        pass
