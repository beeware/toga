from .libs import Gdk, GLib, Gtk


class Icon:
    EXTENSIONS = [".png", ".ico", ".icns"]
    SIZES = None

    def __init__(self, interface, path):
        self.interface = interface
        self.path = path

        try:
            # GtkImage displays its image as an icon, with app-controlled size.
            self.native = Gtk.Image.new_from_paintable(
                Gdk.Texture.new_from_filename(str(path))
            )
        except GLib.GError:
            raise ValueError(f"Unable to load icon from {path}")
