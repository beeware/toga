import warnings

from toga.images import Image
from toga.widgets.base import Widget


class ImageView(Widget):
    """

    Args:
        image (:class:`~toga.images.Image`): The image to display.
        id (str): An identifier for this widget.
        style (:obj:`Style`):

    Todo:
        * Finish implementation.
    """

    def __init__(
        self,
        image=None,
        id=None,
        style=None,
        factory=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style)

        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        self._impl = self.factory.ImageView(interface=self)
        self.image = image

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        if isinstance(image, str):
            self._image = Image(image)
        else:
            self._image = image

        if self._image is not None:
            self._impl.set_image(image)
            self.refresh()

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
