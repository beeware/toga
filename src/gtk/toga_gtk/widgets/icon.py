from gi.repository import Gtk, GdkPixbuf


class Icon:
    EXTENSION = '.icns'

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        # GTK can load ICNS and image files, but doesn't natively scale to the
        # appropriate size as required. So, we help it out. But to avoid loading
        # all the possible icon sizes at once, we lazy load them on first use.
        self.native = {}

    def _native(self, size):
        try:
            return self.native[size]
        except KeyError:
            self.native[size] = Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file(self.interface.filename).scale_simple(size, size, GdkPixbuf.InterpType.BILINEAR)
            )
        return self.native[size]

    native_16 = property(lambda self: self._native(16))
    native_32 = property(lambda self: self._native(32))
    native_48 = property(lambda self: self._native(48))
    native_72 = property(lambda self: self._native(72))
