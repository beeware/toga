from pathlib import Path

from toga_gtk.libs import GdkPixbuf, Gio, GLib


class Image:
    RAW_TYPE = GdkPixbuf.Pixbuf

    def __init__(self, interface, path=None, data=None, raw=None):
        self.interface = interface

        if path:
            try:
                self.native = GdkPixbuf.Pixbuf.new_from_file(str(path))
            except GLib.GError:
                raise ValueError(f"Unable to load image from {path}")
        elif data:
            try:
                input_stream = Gio.MemoryInputStream.new_from_data(data, None)
                self.native = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)
            except GLib.GError:
                raise ValueError("Unable to load image from data")
        else:
            self.native = raw

    def get_width(self):
        return self.native.get_width()

    def get_height(self):
        return self.native.get_height()

    def get_data(self):
        success, buffer = self.native.save_to_bufferv("png")
        if success:
            return buffer
        else:  # pragma: nocover
            # This shouldn't ever happen, and it's difficult to manufacture in test conditions
            raise ValueError("Unable to get PNG data for image")

    def save(self, path):
        path = Path(path)
        try:
            filetype = {
                ".jpg": "jpeg",
                ".jpeg": "jpeg",
                ".png": "png",
                ".bmp": "bmp",
            }[path.suffix.lower()]
            str_path = str(path)
        except KeyError:
            raise ValueError(f"Don't know how to save image of type {path.suffix!r}")

        self.native.savev(str_path, filetype)
