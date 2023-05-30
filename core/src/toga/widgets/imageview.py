from __future__ import annotations

from toga.images import Image
from toga.widgets.base import Widget


class ImageView(Widget):
    """Create a new image view.

    Inherits from :class:`~toga.widgets.base.Widget`.
    """

    def __init__(
        self,
        image: Image | None = None,
        id=None,
        style=None,
    ):
        """
        :param image: The image to display.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        """
        super().__init__(id=id, style=style)
        self._impl = self.factory.ImageView(interface=self)
        self.image = image

    @property
    def image(self) -> Image | None:
        """The image to display."""
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
