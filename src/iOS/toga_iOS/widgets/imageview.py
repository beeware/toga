from toga.interface import ImageView as ImageViewInterface

from ..libs import *
from .base import WidgetMixin


class ImageView(ImageViewInterface, WidgetMixin):
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

        # Add the layout constraints
        self._add_constraints()

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
        self._impl.setFrame_(frame)
        self._impl.setNeedsDisplay()

    def rehint(self):
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            width=fitting_size.width
        )
