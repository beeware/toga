from ..libs import android_widgets
from .base import Widget


class TogaOnClickListener(android_widgets.OnClickListener):
    def __init__(self, imageview_impl):
        super().__init__()
        self.imageview_impl = imageview_impl

    def onClick(self, _view):
        if self.imageview_impl.interface.on_press:
            self.imageview_impl.interface.on_press(widget=self.imageview_impl.interface)


class ImageView(Widget):
    def create(self):
        self.native = android_widgets.ImageView(self._native_activity)
        self.native.setOnClickListener(TogaOnClickListener(imageview_impl=self))

    def set_image(self, image):
        if image and image._impl.native:
            self.native.setImageBitmap(image._impl.native)

    def set_on_press(self, handler):
        # No special handling required
        pass
