from .base import Widget


class ImageView(Widget):
    """

    Args:
        image (:class:`toga.Image`): The image to display.
        id (str): An identifier for this widget.
        style (:obj:`Style`):
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

    Todo:
        * Finish implementation.
    """

    def __init__(self, image=None,
                 id=None, style=None, factory=None, ):
        super().__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.ImageView(interface=self)
        self.image = image

    @property
    def image(self):
        self._impl.get_image()
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        self._impl.set_image(self._image)

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
