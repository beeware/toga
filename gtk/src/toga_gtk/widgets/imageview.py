from ..libs import Gdk, GdkPixbuf, Gtk
from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._image = Gtk.Image()
        self._pixbuf = None
        self.native.add(self._image)

    def set_image(self, image):
        self._pixbuf = image._impl.native

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        # rehint to update scaling of pixbuf
        self.refresh()

    def rehint(self):
        if self._pixbuf:
            height, width = self._resize_max(
                original_height=self._pixbuf.get_height(),
                original_width=self._pixbuf.get_width(),
                max_height=self.native.get_allocated_height(),
                max_width=self.native.get_allocated_width(),
            )

            dpr = self.native.get_scale_factor()

            scaled_pixbuf = self._pixbuf.scale_simple(
                width * dpr, height * dpr, GdkPixbuf.InterpType.BILINEAR
            )

            surface = Gdk.cairo_surface_create_from_pixbuf(
                scaled_pixbuf, 0, self.native.get_window()  # scale: 0 = same as window
            )
            self._image.set_from_surface(surface)

    @staticmethod
    def _resize_max(original_height, original_width, max_height, max_width):
        # Check to make sure all dimensions have valid sizes
        if min(original_height, original_width, max_height, max_width) <= 0:
            return 1, 1

        width_ratio = max_width / original_width
        height_ratio = max_height / original_height

        height = original_height * width_ratio
        if height <= max_height:
            width = original_width * width_ratio
        else:
            height = original_height * height_ratio
            width = original_width * height_ratio

        # On the first display the allocated height/width will be 1x1.
        # If the image isn't square, this will result in one of the dimensions
        # scaling to 0, which breaks GTK. So; constraint the minimum height
        # and width to 1.
        return max(int(height), 1), max(int(width), 1)
