from toga.constants import *
from toga_iOS.libs import UIImageView

from .base import Widget


class ImageView(Widget):

    def create(self):
        self.native = UIImageView.alloc().init()
        self.native.interface = self.interface

        # Disable all autolayout functionality
        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.native.setAutoresizesSubviews_(False)

        self.add_constraints()

        # if self.width is None:
        #     self.width = self._impl.fittingSize().width
        # if self.height is None:
        #     self.height = self._impl.fittingSize().height

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

    def set_frame(self, frame):
        print("SET IMAGE FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
        self.native.setFrame_(frame)
        self.native.setNeedsDisplay()
