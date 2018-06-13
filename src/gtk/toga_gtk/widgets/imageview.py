import os
from urllib.request import Request, urlopen

from gi.repository import GdkPixbuf, Gio, Gtk

import toga

from .base import Widget


class ImageView(Widget):

    def create(self):
        self.native = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._image = Gtk.Image()
        self.native.add(self._image)
        self.native.interface = self.interface

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

        if self.image.path.startswith(('http://', 'https://')):
            request = Request(self.image.path, headers={'User-Agent': ''})
            with urlopen(request) as result:
                input_stream = Gio.MemoryInputStream.new_from_data(result.read(), None)
                self._original_pixbuf = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)
        else:
            full_image_path = self.image.path if os.path.isabs(self.image.path) else os.path.join(toga.App.app_dir, self.image.path)
            if os.path.isfile(full_image_path):
                self._original_pixbuf = GdkPixbuf.Pixbuf.new_from_file(full_image_path)
            else:
                raise ValueError("No image file available at ", full_image_path)
        self.rehint()

    def rehint(self):
        height, width = self._resize_max(
                original_height=self._original_pixbuf.get_height(),
                original_width=self._original_pixbuf.get_width(),
                max_height=self.native.get_allocated_height(),
                max_width=self.native.get_allocated_width())

        pixbuf = self._original_pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        self._image.set_from_pixbuf(pixbuf)

    @staticmethod
    def _resize_max(original_height, original_width, max_height, max_width):

        # Check to make sure all dimensions have valid sizes
        if min(original_height, original_width, max_height, max_width) <= 0:
            return 1, 1

        width_ratio = max_width/original_width
        height_ratio = max_height/original_height

        height = original_height * width_ratio
        if height <= max_height:
            width = original_width * width_ratio
        else:
            height = original_height * height_ratio
            width = original_width * height_ratio

        return int(height), int(width)
