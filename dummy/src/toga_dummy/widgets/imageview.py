from ..utils import not_required
from .base import Widget


@not_required  # Testbed coverage is complete
class ImageView(Widget):
    def create(self):
        self._action("create ImageView")

    def set_image(self, image):
        self._action("set image", image=image)
