from toga.widgets.imageview import rehint_imageview

from ..libs import GdkPixbuf, Gtk
from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = Gtk.Image()
        self._aspect_ratio = None

    def set_image(self, image):
        if image:
            self.native.set_from_pixbuf(image._impl.native)
        else:
            self.native.set_from_pixbuf(None)

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        # GTK doesn't have any native image resizing; we need to manually
        # scale the native pixbuf to the preferred size as a result of
        # resizing the image.
        if self.interface.image:
            if self._aspect_ratio is None:
                # Don't preserve aspect ratio; image fits the available space.
                image_width = width
                image_height = height
            else:
                # Determine what the width/height of the image would be
                # preserving the aspect ratio. If the scaled size exceeds
                # the allocated size, then that isn't the dimension
                # being preserved.
                candidate_width = int(height * self._aspect_ratio)
                candidate_height = int(width / self._aspect_ratio)
                if candidate_width > width:
                    image_width = width
                    image_height = candidate_height
                else:
                    image_width = candidate_width
                    image_height = height

            # Minimum image size is 1x1
            image_width = max(1, image_width)
            image_height = max(1, image_height)

            # Scale the pixbuf to fit the provided space.
            scaled = self.interface.image._impl.native.scale_simple(
                image_width, image_height, GdkPixbuf.InterpType.BILINEAR
            )

            self.native.set_from_pixbuf(scaled)

    def rehint(self):
        width, height, self._aspect_ratio = rehint_imageview(
            image=self.interface.image,
            style=self.interface.style,
        )
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
