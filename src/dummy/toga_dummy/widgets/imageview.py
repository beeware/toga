from .base import Widget


class ImageView(Widget):
    def create(self):
        self._action('create ImageView')

    def set_image(self, image):
        self._set_value('image', image)
