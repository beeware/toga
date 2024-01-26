from toga.widgets.imageview import rehint_imageview

from ..libs import Gdk, GdkPixbuf, Gtk
from .base import Widget


class TogaPicture(Gtk.Picture):
    def do_size_allocate(self, width, height, baseline):
        Gtk.Picture.do_size_allocate(self, width, height, baseline)
        if self.interface.image:
            self._impl.set_scaled_pixbuf(self.interface.image, width, height)


class ImageView(Widget):
    def create(self):
        self.native = TogaPicture
        self._aspect_ratio = None

    def set_image(self, image):
        if image:
            self.set_scaled_pixbuf(
                image,
                self.native.compute_bounds(self.native)[1].size.width,
                self.native.compute_bounds(self.native)[1].size.height,
            )
        else:
            self.native.set_paintable(None)

    def set_scaled_pixbuf(self, image, width, height):
        if self._aspect_ratio is None:
            # Don't preserve aspect ratio; image fits the available space.
            self.native.set_content_fit(Gtk.ContentFit.FILL)
            image_width = width
            image_height = height
        else:
            # Determine what the width/height of the image would be
            # preserving the aspect ratio. If the scaled size exceeds
            # the allocated size, then that isn't the dimension
            # being preserved.
            self.native.set_content_fit(Gtk.ContentFit.CONTAIN)
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
        scaled = image._impl.native.scale_simple(
            image_width, image_height, GdkPixbuf.InterpType.BILINEAR
        )

        self.native.set_paintable(Gdk.Texture.new_for_pixbuf(scaled))

    def rehint(self):
        width, height, self._aspect_ratio = rehint_imageview(
            image=self.interface.image,
            style=self.interface.style,
        )
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
