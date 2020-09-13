from .libs.android_widgets import BitmapFactory


class Image:
    def __init__(self, interface, path=None, url=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = BitmapFactory.decodeFile(str(path))
        elif url:
            # Android BitmapFactory nor ImageView provide a convenient async way to fetch images by URL
            self.native = None
