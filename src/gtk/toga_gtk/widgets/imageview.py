
from ..libs import GdkPixbuf, Gtk
from .base import Widget


class ImageView(Widget):

    def create(self):
        self.native = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._image = Gtk.Image()
        self._pixbuf = None
        self.native.add(self._image)
        self.native.interface = self.interface

    def set_image(self, image):
        self._pixbuf = image._impl.native

    def rehint(self):
        height, width = self._resize_max(
            original_height=self._pixbuf.get_height(),
            original_width=self._pixbuf.get_width(),
            max_height=self.native.get_allocated_height(),
            max_width=self.native.get_allocated_width()
        )

        scaled_pixbuf = self._pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        self._image.set_from_pixbuf(scaled_pixbuf)

    @staticmethod
    def _resize_max(original_height, original_width, max_height, max_width):

        # Check to make sure all dimensions have valid sizes
        if min(original_height, original_width, max_height, max_width) <= 0:
            return 1, 1

        width_ratio = max_width/original_width
        height_ratio = max_height/original_height

        height = original_height * width_ratio
        if height <= max_height:
            width = original_width * width_ratio
        else:
            height = original_height * height_ratio
            width = original_width * height_ratio

        return int(height), int(width)
