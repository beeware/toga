from gi.repository import Gtk, GdkPixbuf


class Icon:
    EXTENSION = '.icns'

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.native = None

        # GTK can load ICNS and image files, but doesn't natively scale to the
        # appropriate size as required. So, we help it out. But to avoid loading
        # all the possible icon sizes at once, we lazy load them on first use.
        self._filename = interface.filename
        self._impl_cache = {}

    def __impl(self, size):
        try:
            return self._impl_cache[size]
        except KeyError:
            self._impl_cache[size] = Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file(self._filename).scale_simple(size, size, GdkPixbuf.InterpType.BILINEAR)
            )
        return self._impl_cache[size]

    _impl_16 = property(lambda self: self.__impl(16))
    _impl_32 = property(lambda self: self.__impl(32))
    _impl_48 = property(lambda self: self.__impl(48))
    _impl_72 = property(lambda self: self.__impl(72))
