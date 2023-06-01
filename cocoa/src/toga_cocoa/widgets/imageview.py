from travertino.size import at_least

from toga.style.pack import COLUMN
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
            if style.width and style.height:
                # Explicit width and height for image. Scale the rendered image
                # to fit the explicitly provided size.
                width = style.width
                height = style.height
                self.native.imageScaling = NSImageScaleAxesIndependently
            elif style.width:
                # Explicit width, implicit height. Preserve aspect ratio.
                width = style.width
                height = style.width * image.size.height // image.size.width
                self.native.imageScaling = NSImageScaleProportionallyUpOrDown
            elif style.height:
                # Explicit height, implicit width. Preserve aspect ratio.
                width = style.height * image.size.width // image.size.height
                height = style.height
                self.native.imageScaling = NSImageScaleProportionallyUpOrDown
            else:
                # Use the image's actual size.
                width = image.size.width
                height = image.size.height
                self.native.imageScaling = NSImageScaleProportionallyUpOrDown

            if style.flex and self.interface.parent:
                parent_style = self.interface.parent.style
                if parent_style.direction == COLUMN:
                    # A flex-sized image in a column box
                    self.interface.intrinsic.width = at_least(width)
                    self.interface.intrinsic.height = at_least(0)
                else:
                    # A flex-sized image in a row box
                    self.interface.intrinsic.width = at_least(0)
                    self.interface.intrinsic.height = at_least(height)
            else:
                # A fixed-size image, or a flex image that hasn't been placed yet
                self.interface.intrinsic.width = width
                self.interface.intrinsic.height = height
        else:
            # No image. Hinted size is 0.
            self.interface.intrinsic.width = 0
            self.interface.intrinsic.height = 0
