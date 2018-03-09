from toga.constants import *
from toga_iOS.libs import (
    UIImageView,
    UIViewContentMode
)
from .base import Widget


class ImageView(Widget):

    def create(self):
        self.native = UIImageView.alloc().init()
        self.native.interface = self.interface
        self.native.contentMode = UIViewContentMode.ScaleAspectFit
        self.native.clipsToBounds = 1

        # Disable all autolayout functionality
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.native.setAutoresizesSubviews_(False)

        self.add_constraints()

    def get_image(self):
        return self.native.image

    def set_image(self, image):
        if image:
            self.native.image = image._impl.native
        else:
            self.native.image = None
