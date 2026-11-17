from pathlib import Path

from toga.images import ImageLoadError
from toga_gtk.libs import GdkPixbuf, Gio, GLib


class Image:
    RAW_TYPE = GdkPixbuf.Pixbuf

    def __init__(self, interface, data=None, raw=None):
        self.interface = interface

        if data:
            try:
                input_stream = Gio.MemoryInputStream.new_from_bytes(
                    GLib.Bytes.new(data)
                )
                self.native = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)
            except GLib.GError as exc:
                raise ImageLoadError from exc
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
            # This shouldn't ever happen, and it's difficult to manufacture
            # in test conditions
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
        except KeyError as exc:
            raise ValueError(
                f"Don't know how to save image of type {path.suffix!r}"
            ) from exc

        native = self.native
        if filetype == "jpeg" and native.get_has_alpha():
            # JPEG can't store alpha, and glycin-based encoders reject RGBA input.
            width, height = native.get_width(), native.get_height()
            rgb = GdkPixbuf.Pixbuf.new(
                GdkPixbuf.Colorspace.RGB, False, 8, width, height
            )
            native.composite(
                rgb, 0, 0, width, height, 0, 0, 1, 1, GdkPixbuf.InterpType.NEAREST, 255
            )
            native = rgb
        native.savev(str_path, filetype)
