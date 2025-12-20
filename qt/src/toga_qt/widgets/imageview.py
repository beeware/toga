from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel
from travertino.constants import TRANSPARENT

from toga.widgets.imageview import rehint_imageview

from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = QLabel()
        self.native.setAlignment(Qt.AlignCenter)
        self._aspect_ratio = None
        self.native.setAutoFillBackground(True)
        # Background is not autofilled by default; but since we're
        # enabling it here, let the default color be transparent
        # so it autofills nothing by default.
        self._default_background_color = TRANSPARENT

    def set_image(self, image):
        if image:
            self.set_scaled_pixbuf(image._impl.native)
        else:
            self.native.setPixmap(QPixmap())

    def set_scaled_pixbuf(self, image):
        scaled = QPixmap.fromImage(image).scaled(
            self.native.size(),
            Qt.KeepAspectRatio if self._aspect_ratio else Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation,
        )
        self.native.setPixmap(scaled)

    def set_bounds(self, *args):
        super().set_bounds(*args)
        if self.interface.image:
            self.set_scaled_pixbuf(self.interface.image._impl.native)

    def rehint(self):
        width, height, self._aspect_ratio = rehint_imageview(
            image=self.interface.image, style=self.interface.style
        )
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
