import os

from gi.repository import Gtk, GdkPixbuf

import toga


class Icon(object):
    app_icon = None

    def __init__(self, path, system=False):
        self.path = path
        self.system = system

        if self.system:
            self._filename = os.path.join(os.path.dirname(toga.__file__), 'resources', self.path)
        else:
            self._filename = self.path

        # GTK can load ICNS and image files, but doesn't natively scale to the
        # appropriate size as required. So, we help it out. But to avoid loading
        # all the possible icon sizes at once, we lazy load them on first use.
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

    @staticmethod
    def load(path_or_icon, default=None):
        if path_or_icon:
            if isinstance(path_or_icon, Icon):
                obj = path_or_icon
            else:
                obj = Icon(path_or_icon)
        elif default:
            obj = default
        return obj


TIBERIUS_ICON = Icon('tiberius.icns', system=True)
