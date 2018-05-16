#FIXME: Image alignment is still wrong
#FIXME: Image resizing is still wrong

import os
from urllib.request import Request, urlopen

from gi.repository import Gtk, GdkPixbuf, Gio

import toga
from .base import Widget

class ImageView(Widget):

    def create(self):
        self.native = Gtk.Image()
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
        elif os.path.isabs(self.image.path):
            self._original_pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.image.path)
        else:
            self._original_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(toga.App.app_dir, self.image.path))

        self.interface.style.update(height=self._original_pixbuf.get_height(), width=self._original_pixbuf.get_width())
        self.native.set_asignment

        self.rehint()

    def rehint(self):
        width = self.native.get_allocated_width()
        height = self.native.get_allocated_height()

        pixbuf = self._original_pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.NEAREST)
        self.native.set_from_pixbuf(pixbuf)
