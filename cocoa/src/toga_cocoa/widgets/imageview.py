from travertino.size import at_least

from toga.style.pack import NONE
from toga_cocoa.libs import (
    NSImageAlignment,
    NSImageFrameNone,
    NSImageScaleAxesIndependently,
    NSImageScaleProportionallyUpOrDown,
    NSImageView,
)

from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = NSImageView.alloc().init()

        # self.native.imageFrameStyle = NSImageFrameGrayBezel
        self.native.imageFrameStyle = NSImageFrameNone
        self.native.imageAlignment = NSImageAlignment.Center.value
        self.native.imageScaling = NSImageScaleAxesIndependently

        # Add the layout constraints
        self.add_constraints()

    def set_image(self, image):
        if image:
            self.native.image = self.interface.image._impl.native
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
                self.native.imageScaling = NSImageScaleAxesIndependently
            elif style.width != NONE:
                # Explicit width, implicit height. Preserve aspect ratio.
                width = style.width
                height = style.width * image.size.height // image.size.width
                if style.flex:
                    height = at_least(height)
                self.native.imageScaling = NSImageScaleProportionallyUpOrDown
            elif style.height != NONE:
                # Explicit height, implicit width. Preserve aspect ratio.
                width = style.height * image.size.width // image.size.height
                height = style.height
                if style.flex:
                    width = at_least(width)
                self.native.imageScaling = NSImageScaleProportionallyUpOrDown
            else:
                # Use the image's actual size.
                width = image.size.width
                height = image.size.height
                if style.flex:
                    width = at_least(width)
                    height = at_least(height)
                self.native.imageScaling = NSImageScaleProportionallyUpOrDown

            self.interface.intrinsic.width = width
            self.interface.intrinsic.height = height
        else:
            # No image. Hinted size is 0.
            self.interface.intrinsic.width = 0
            self.interface.intrinsic.height = 0
            self.native.imageScaling = NSImageScaleAxesIndependently
