from travertino.size import at_least

from toga.style.pack import NONE
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

        self.add_constraints()

    def set_image(self, image):
        if image:
            self.native.image = image._impl.native
        else:
            self.native.image = None

    def rehint(self):
        image = self.native.image
        if image:
            style = self.interface.style
            if style.width != NONE and style.height != NONE:
                # Explicit width and height for image. Scale the rendered image
                # to fit the explicitly provided size.
                width = style.width
                height = style.height
                self.native.contentMode = UIViewContentMode.ScaleToFill
            elif style.width != NONE:
                # Explicit width, implicit height. Preserve aspect ratio.
                width = style.width
                height = style.width * image.size.height // image.size.width
                if style.flex:
                    height = at_least(height)
                self.native.contentMode = UIViewContentMode.ScaleAspectFit
            elif style.height != NONE:
                # Explicit height, implicit width. Preserve aspect ratio.
                width = style.height * image.size.width // image.size.height
                height = style.height
                if style.flex:
                    width = at_least(width)
                self.native.contentMode = UIViewContentMode.ScaleAspectFit
            else:
                # Use the image's actual size.
                width = image.size.width
                height = image.size.height
                if style.flex:
                    width = at_least(width)
                    height = at_least(height)
                self.native.contentMode = UIViewContentMode.ScaleAspectFit

            self.interface.intrinsic.width = width
            self.interface.intrinsic.height = height
        else:
            # No image. Hinted size is 0.
            self.interface.intrinsic.width = 0
            self.interface.intrinsic.height = 0
            self.native.contentMode = UIViewContentMode.ScaleToFill
