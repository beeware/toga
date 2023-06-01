from __future__ import annotations

from pathlib import Path

from toga.images import Image
from toga.widgets.base import Widget


class ImageView(Widget):
    def __init__(
        self,
        image: Image | Path | str | None = None,
        id=None,
        style=None,
    ):
        """
        Create a new image view.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param image: The image to display.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        """
        super().__init__(id=id, style=style)
        # Prime the image attribute
        self._image = None
        self._impl = self.factory.ImageView(interface=self)
        self.image = image

    @property
    def image(self) -> Image | None:
        """The image to display."""
        return self._image

    @image.setter
    def image(self, image):
        if isinstance(image, Image):
            self._image = image
        elif image is None:
            self._image = None
        else:
            self._image = Image(image)

        self._impl.set_image(self._image)
        self.refresh()
