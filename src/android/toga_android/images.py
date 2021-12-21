from .libs.android.graphics import BitmapFactory, Bitmap
from rubicon.java.jni import java


class Image:
    def __init__(self, interface, path=None, url=None):
        self.interface = interface
        self.path = path
        self.url = url

        if path:
            self.native = Bitmap(__jni__ = java.NewGlobalRef(BitmapFactory.decodeFile(str(path))))
        elif url:
            # Android BitmapFactory nor ImageView provide a convenient async way to fetch images by URL
            self.native = None
