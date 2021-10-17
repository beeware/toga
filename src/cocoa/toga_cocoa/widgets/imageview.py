from rubicon.objc.api import objc_method
from toga_cocoa.libs import (
    NSImage,
    NSImageAlignment,
    NSImageFrameNone,
    NSImageScaleProportionallyUpOrDown,
    NSImageView,
    NSSize
)

from .base import Widget


class TogaImageView(NSImageView):
    @objc_method
    def mouseDown_(self, event) -> None:
        if self.interface.on_press:
            self.interface.on_press(self.interface)


class ImageView(Widget):

    def create(self):
        self.native = TogaImageView.alloc().init()
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

    def set_on_press(self, handler):
        pass

    def rehint(self):
        pass
