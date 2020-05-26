from toga_cocoa.libs import (
    NSImage,
    NSImageAlignment,
    NSImageFrameNone,
    NSImageScaleProportionallyUpOrDown,
    NSImageView,
    NSSize
)

from .base import Widget


class ImageView(Widget):

    def create(self):
        self.native = NSImageView.alloc().init()
        self.native.interface = self.interface

        # self._impl.imageFrameStyle = NSImageFrameGrayBezel
        self.native.imageFrameStyle = NSImageFrameNone
        self.native.imageAlignment = NSImageAlignment.Center.value
        self.native.imageScaling = NSImageScaleProportionallyUpOrDown

        # Add the layout constraints
        self.add_constraints()

    def set_image(self, image):
        if image:
            self.native.image = self.interface._image._impl.native
        else:
            width = 0
            height = 0
            if self.interface.style.width:
                width = self.interface.style.width
            if self.interface.style.height:
                height = self.interface.style.height

            self.native.image = NSImage.alloc().initWithSize(NSSize(width, height))

    def rehint(self):
        pass

