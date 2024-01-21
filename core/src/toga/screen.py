from typing import Tuple

from toga.images import Image
from toga.platform import get_platform_factory


class Screen:
    def __init__(self, _impl):
        self._impl = _impl
        self.factory = get_platform_factory()

    @property
    def name(self) -> str:
        """Unique name of the screen."""
        return self._impl.get_name()

    @property
    def origin(self) -> Tuple[int, int]:
        """The absolute coordinates of the screen's origin, as a ``(x, y)`` tuple."""
        return self._impl.get_origin()

    @property
    def size(self) -> Tuple[int, int]:
        """The size of the screen, as a ``(width, height)`` tuple."""
        return self._impl.get_size()

    def as_image(self, format=Image) -> Image:
        """Render the current contents of the screen as an image.

        :param format: Format to provide. Defaults to :class:`~toga.images.Image`; also
            supports :any:`PIL.Image.Image` if Pillow is installed
        :returns: An image containing the screen content, in the format requested.
        """
        return Image(self._impl.get_image_data()).as_format(format)
