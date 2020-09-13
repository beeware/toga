from ..libs import android_widgets
from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = android_widgets.ImageView(self._native_activity)

    def set_image(self, image):
        if image and image._impl.native:
            self.native.setImageBitmap(image._impl.native)
