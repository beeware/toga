from __future__ import annotations

from typing import TYPE_CHECKING

from toga.images import Image
from toga.platform import get_platform_factory

if TYPE_CHECKING:
    from toga.images import ImageT


class Screen:
    def __init__(self, _impl):
        self._impl = _impl
        self.factory = get_platform_factory()

    @property
    def name(self) -> str:
        """Unique name of the screen."""
        return self._impl.get_name()

    @property
    def origin(self) -> tuple[int, int]:
        """The absolute coordinates of the screen's origin, as a ``(x, y)`` tuple."""
        return self._impl.get_origin()

    @property
    def size(self) -> tuple[int, int]:
        """The size of the screen, as a ``(width, height)`` tuple."""
        return self._impl.get_size()

    def as_image(self, format: type[ImageT] = Image) -> ImageT:
        """Render the current contents of the screen as an image.

        :param format: Format to provide. Defaults to :class:`~toga.images.Image`; also
            supports :any:`PIL.Image.Image` if Pillow is installed, as well as any image
            types defined by installed :doc:`image format plugins
            </reference/plugins/image_formats>`.
        :returns: An image containing the screen content, in the format requested.
        """
        return Image(self._impl.get_image_data()).as_format(format)
