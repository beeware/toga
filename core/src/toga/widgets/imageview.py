from __future__ import annotations

from pathlib import Path

from travertino.size import at_least

from toga.images import Image
from toga.style.pack import NONE
from toga.widgets.base import Widget


def rehint_imageview(image, style, scale=1):
    """Compute the size hints for an ImageView based on the image.

    This logic is common across all backends, so it's shared here.

    :param image: The image being displayed.
    :param style: The style object for the imageview.
    :param scale: The scale factor (if any) to apply to native pixel sizes.
    :returns: A triple containing the intrinsic width hint, intrinsic height
        hint, and a boolean describing whether the ImageView should preserve
        the image's aspect ratio when rendering.
    """
    if image:
        if style.width != NONE and style.height != NONE:
            # Explicit width and height for image. Scale the rendered image
            # to fit the explicitly provided size.
            width = style.width * scale
            height = style.height * scale
            preserve_aspect_ratio = False

        elif style.width != NONE:
            # Explicit width, implicit height. Preserve aspect ratio.
            width = style.width * scale
            height = style.width * scale * image.height // image.width
            if style.flex:
                height = at_least(height)
            preserve_aspect_ratio = True
        elif style.height != NONE:
            # Explicit height, implicit width. Preserve aspect ratio.
            width = style.height * scale * image.width // image.height
            height = style.height * scale
            if style.flex:
                width = at_least(width)
            preserve_aspect_ratio = True
        else:
            # Use the image's actual size.
            width = image.width * scale
            height = image.height * scale
            if style.flex:
                width = at_least(width)
                height = at_least(height)
            preserve_aspect_ratio = True
    else:
        # No image. Hinted size is 0.
        width = 0
        height = 0
        preserve_aspect_ratio = False

    return width, height, preserve_aspect_ratio


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
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?

        ImageView widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value):
        pass

    def focus(self):
        "No-op; ImageView cannot accept input focus"
        pass

    @property
    def image(self) -> Image | None:
        """The image to display.

        When setting an image, you can provide a:
         * A :class:`~toga.images.Image` instance; pr
         * Any value that would be a valid path specifier when creating an new :class:`~toga.images.Image` instance; or
         * :any:`None` to clear to image view.
        """
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
