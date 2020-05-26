from urllib.request import Request, urlopen

from toga_gtk.libs import GdkPixbuf, Gio


class Image:
    def __init__(self, interface, path=None, url=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = GdkPixbuf.Pixbuf.new_from_file(str(path))
        else:
            request = Request(url, headers={'User-Agent': ''})
            with urlopen(request) as result:
                input_stream = Gio.MemoryInputStream.new_from_data(result.read(), None)
                self.native = GdkPixbuf.Pixbuf.new_from_stream(input_stream, None)
