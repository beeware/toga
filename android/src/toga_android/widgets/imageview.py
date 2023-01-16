from ..libs.android.widget import ImageView as A_ImageView
from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = A_ImageView(self._native_activity)

    def set_image(self, image):
        if image and image._impl.native:
            self.native.setImageBitmap(image._impl.native)
