import os

from toga import App
from .libs import Gtk, GdkPixbuf


class Icon:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        # GTK can load ICNS and image files, but doesn't natively scale to the
        # appropriate size as required. So, we help it out. We pre-populate
        # the image cache to ensure the binding is successful, and an icons
        # of all the required sizes are availble (and if they're not, it will
        # stimulate fallback logic)
        self.native = {}
        self._native(32)
        self._native(72)

    def _native(self, size):
        try:
            return self.native[size]
        except KeyError:
            basename, file_extension = os.path.splitext(self.interface.filename)

            # The final icon path is relative to the app.
            app_path = App.app.paths.app

            if not file_extension:
                # If no extension is provided, look for one of the allowed
                # icon types, in preferred format order.
                for extension in ['.png', '.ico', '.icns']:
                    file_path = app_path / ('{basename}-{size}{extension}'.format(
                        basename=basename,
                        size=size,
                        extension=extension
                    ))
                    if file_path.exists():
                        break

                    file_path = app_path / (basename + extension)
                    if file_path.exists():
                        break
            elif file_extension in ['.png', '.ico', '.icns']:
                file_path = app_path / self.interface.filename
            else:
                # An icon has been specified, but it's not a valid format.
                raise FileNotFoundError(
                    "[GTK+] {filename} is not a valid icon".format(
                        filename=self.interface.filename
                    )
                )

            if file_path.exists():
                self.native[size] = Gtk.Image.new_from_pixbuf(
                    GdkPixbuf.Pixbuf.new_from_file(str(file_path)).scale_simple(
                        size, size, GdkPixbuf.InterpType.BILINEAR)
                )
            else:
                raise FileNotFoundError(
                    "[GTK+] Can't find icon {filename}".format(
                        filename=self.interface.filename
                    )
                )

        return self.native[size]

    native_32 = property(lambda self: self._native(32))
    native_72 = property(lambda self: self._native(72))
