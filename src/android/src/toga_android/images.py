from .libs.android.graphics import BitmapFactory


class Image:
    def __init__(self, interface, path=None, url=None, data=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = BitmapFactory.decodeFile(str(path))
        elif url:
            # Android BitmapFactory nor ImageView provide a convenient async way to fetch images by URL
            self.native = None
        elif data:
            self.native = BitmapFactory.decodeByteArray(data, 0, len(data))
