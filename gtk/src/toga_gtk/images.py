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
        self.interface.factory.not_implemented("Image.save()")
