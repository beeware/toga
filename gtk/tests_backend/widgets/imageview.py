from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = Gtk.Image if GTK_VERSION < (4, 0, 0) else Gtk.Picture

    @property
    def preserve_aspect_ratio(self):
        if GTK_VERSION >= (4, 8, 0):
            return self.native.get_content_fit() == Gtk.ContentFit.CONTAIN
        elif GTK_VERSION >= (4, 0, 0):
            return self.native.get_keep_aspect_ratio()
        else:
            return self.impl._aspect_ratio is not None

    def assert_image_size(self, width, height):
        if GTK_VERSION < (4, 0, 0):
            # Confirm the pixelbuf has been scaled to the appropriate size.
            pixbuf = self.native.get_pixbuf()
            assert (pixbuf.get_width(), pixbuf.get_height()) == (width, height)
        else:
            # Inspect the bounds of the image actually rendered by Gtk.Picture.
            snapshot = Gtk.Snapshot()
            paintable = Gtk.WidgetPaintable.new(self.native)
            paintable.snapshot(snapshot, self.width, self.height)
            bounds = snapshot.to_node().get_bounds()
            assert (bounds.get_width(), bounds.get_height()) == (width, height)
