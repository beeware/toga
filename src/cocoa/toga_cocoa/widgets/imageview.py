from toga_cocoa.libs import *

from .base import Widget


class ImageView(Widget):

    def create(self):
        self.native = NSImageView.alloc().init()
        self.native.interface = self.interface

        # self._impl.imageFrameStyle = NSImageFrameGrayBezel
        self.native.imageFrameStyle = NSImageFrameNone
        self.native.imageAlignment = NSImageAlignCenter
        self.native.imageScaling = NSImageScaleProportionallyUpOrDown

        # self._impl.setWantsLayer_(True)
        # self._impl.setBackgroundColor_(NSColor.blueColor)

        # if self.width is None:
        #     self.width = self._impl.fittingSize().width
        # if self.height is None:
        #     self.height = self._impl.fittingSize().height

        # Add the layout constraints
        self.add_constraints()

    # @property
    # def alignment(self):
    #     return self._alignment

    # @alignment.setter
    # def alignment(self, value):
    #     self._alignment = value
    #     self._impl.setAlignment_(NSTextAlignment(self._alignment))

    # @property
    # def scaling(self):
    #     return self._scaling

    # @scaling.setter
    # def scaling(self, value):
    #     self._scaling = value
    #     self._impl.setAlignment_(NSTextAlignment(self._scaling))

    def get_image(self):
        return self.native.image

    def set_image(self, image):
        if image:
            self.native.image = image._impl.native
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

