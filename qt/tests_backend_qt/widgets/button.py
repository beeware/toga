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
        # No assertion needed here.  It is handled by theme.
        # [better not write anything more here just in case of
        # anything about size accidentally being an inappropriate
        # joke]
        pass
