from toga.widgets.imageview import rehint_imageview
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
        width, height, aspect_ratio = rehint_imageview(
            image=self.interface.image,
            style=self.interface.style,
        )
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
        if aspect_ratio is not None:
            self.native.imageScaling = NSImageScaleProportionallyUpOrDown
        else:
            self.native.imageScaling = NSImageScaleAxesIndependently
