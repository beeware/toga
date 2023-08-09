from .images import Image


class Screen:
    def __init__(self, _impl):
        self._impl = _impl

    @property
    def name(self):
        """Unique name of the screen."""
        return self._impl.get_name()

    @property
    def origin(self):
        """The absolute coordinates of the screen's origin, as a ``(x, y)`` tuple."""
        return self._impl.get_origin()

    @property
    def size(self):
        """The size of the screen, as a ``(width, height)`` tuple."""
        return self._impl.get_size()

    def as_image(self):
        return Image(data=self._impl.get_image_data())
