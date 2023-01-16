from urllib.request import Request, urlopen

from toga_gtk.libs import GdkPixbuf, Gio


class Image:
    def __init__(self, interface, path=None, url=None, data=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = GdkPixbuf.Pixbuf.new_from_file(str(path))
        elif url:
            request = Request(url, headers={"User-Agent": ""})
            with urlopen(request) as result:
                input_stream = Gio.MemoryInputStream.new_from_data(result.read(), None)
                self.native = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)
        elif data:
            input_stream = Gio.MemoryInputStream.new_from_data(data, None)
            self.native = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)

    def save(self, path):
        self.interface.factory.not_implemented("Image.save()")
