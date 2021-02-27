from toga.handlers import wrapped_handler
from toga.images import Image
from toga.widgets.base import Widget

class ImageView(Widget):
    """

    Args:
        image (:class:`toga.Image`): The image to display.
        id (str): An identifier for this widget.
        style (:obj:`Style`):
        on_press (:obj:`callable`): Function to execute when ImageView is pressed.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)

    Todo:
        * Finish implementation.
    """

    def __init__(
        self, image=None,
        id=None, style=None, on_press=None, factory=None
    ):
        super().__init__(id=id, style=style, factory=factory)

        # Set all the properties
        self._impl = self.factory.ImageView(interface=self)
        self.image = image
        self.on_press = on_press

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
            # Bind the image to the widget's factory.
            self._image.bind(self.factory)

            self._impl.set_image(image)
            self._impl.rehint()

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
    def on_press(self):
        """The handler to invoke when the ImageView is pressed.

        Returns:
            The function ``callable`` that is called on ImageView press.
        """
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        """Set the handler to invoke when the ImageView is pressed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the ImageView is pressed.
        """
        self._on_press = wrapped_handler(self, handler)
        self._impl.set_on_press(self._on_press)
