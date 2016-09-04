from ..libs import *
from .base import Widget
from toga.constants import *


class ImageView(Widget):
    def __init__(self, image=None, style=None):
        super().__init__(style=style)

        self.startup()

        self.image = image

    def startup(self):
        self._impl = UIImageView.alloc().init()
        self._impl.interface = self

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

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

    @property
    def image(self):
        return self._impl.image

    @image.setter
    def image(self, image):
        if image:
            self._impl.image = image._impl

    def _set_frame(self, frame):
        print("SET IMAGE FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
        self._impl.setFrame_(frame)
        self._impl.setNeedsDisplay()
