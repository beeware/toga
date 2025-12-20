from PySide6.QtWidgets import QLabel

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = QLabel

    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.autoFillBackground()

    @property
    def preserve_aspect_ratio(self):
        return self.impl._aspect_ratio is not None

    def assert_image_size(self, width, height):
        pixmap = self.native.pixmap()
        assert (pixmap.width(), pixmap.height()) == (width, height)
