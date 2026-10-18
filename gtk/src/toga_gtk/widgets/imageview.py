from toga.widgets.imageview import rehint_imageview

from ..libs import GTK_VERSION, Gdk, GdkPixbuf, GLib, Gtk
from .base import Widget


class ImageView(Widget):
    def create(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native = Gtk.Image()
            self.native.connect("size-allocate", self.gtk_size_allocate)
        else:  # pragma: no-cover-if-gtk3
            self.native = Gtk.Picture(can_shrink=True)
        self._aspect_ratio = None

    def set_image(self, image):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            if image:
                self.set_scaled_pixbuf(image._impl.native, self.native.get_allocation())
            else:
                self.native.set_from_pixbuf(None)
        else:  # pragma: no-cover-if-gtk3
            if image:
                pixbuf = image._impl.native
                self.native.set_paintable(
                    Gdk.MemoryTexture.new(
                        pixbuf.get_width(),
                        pixbuf.get_height(),
                        Gdk.MemoryFormat.R8G8B8A8
                        if pixbuf.get_has_alpha()
                        else Gdk.MemoryFormat.R8G8B8,
                        GLib.Bytes.new(pixbuf.get_pixels()),
                        pixbuf.get_rowstride(),
                    )
                )
            else:
                self.native.set_paintable(None)

    def gtk_size_allocate(self, widget, allocation):
        # GTK doesn't have any native image resizing; so, when the Gtk.Image
        # has a new size allocated, we need to manually scale the native pixbuf
        # to the preferred size as a result of resizing the image.
        if self.interface.image:
            self.set_scaled_pixbuf(self.interface.image._impl.native, allocation)

    def set_scaled_pixbuf(self, image, allocation):
        if self._aspect_ratio is None:
            # Don't preserve aspect ratio; image fits the available space.
            image_width = allocation.width
            image_height = allocation.height
        else:
            # Determine what the width/height of the image would be
            # preserving the aspect ratio. If the scaled size exceeds
            # the allocated size, then that isn't the dimension
            # being preserved.
            candidate_width = int(allocation.height * self._aspect_ratio)
            candidate_height = int(allocation.width / self._aspect_ratio)
            if candidate_width > allocation.width:
                image_width = allocation.width
                image_height = candidate_height
            else:
                image_width = candidate_width
                image_height = allocation.height

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
        if GTK_VERSION >= (4, 8, 0):  # pragma: no-cover-if-gtk3
            self.native.set_content_fit(
                Gtk.ContentFit.CONTAIN
                if self._aspect_ratio is not None
                else Gtk.ContentFit.FILL
            )
        elif GTK_VERSION >= (4, 0, 0):  # pragma: no-cover-if-gtk3
            self.native.set_keep_aspect_ratio(self._aspect_ratio is not None)
