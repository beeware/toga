from pathlib import Path

from toga_gtk.libs import GdkPixbuf, Gio


class Image:
    def __init__(self, interface, path=None, data=None):
        self.interface = interface

        if path:
            self.native = GdkPixbuf.Pixbuf.new_from_file(str(path))
        else:
            input_stream = Gio.MemoryInputStream.new_from_data(data, None)
            self.native = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)

    def get_width(self):
        return self.native.get_width()

    def get_height(self):
        return self.native.get_height()

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
