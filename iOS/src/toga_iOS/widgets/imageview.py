from toga.colors import TRANSPARENT
from toga.widgets.imageview import rehint_imageview
from toga_iOS.libs import UIImageView, UIViewContentMode
from toga_iOS.widgets.base import Widget


class ImageView(Widget):
    def create(self):
        self.native = UIImageView.alloc().init()
        self.native.contentMode = UIViewContentMode.ScaleAspectFit
        self.native.clipsToBounds = 1

        # Disable all autolayout functionality
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.native.setAutoresizesSubviews_(False)

        self._default_background_color = TRANSPARENT

        self.add_constraints()

    def set_image(self, image):
        if image:
            self.native.image = image._impl.native
        else:
            self.native.image = None

    def rehint(self):
        width, height, aspect_ratio = rehint_imageview(
            image=self.interface.image,
            style=self.interface.style,
        )
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
        if aspect_ratio is not None:
            self.native.contentMode = UIViewContentMode.ScaleAspectFit
        else:
            self.native.contentMode = UIViewContentMode.ScaleToFill
