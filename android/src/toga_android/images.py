from .libs.android.graphics import BitmapFactory


class Image:
    def __init__(self, interface, path=None, data=None):
        self.interface = interface

        if path:
            self.native = BitmapFactory.decodeFile(str(path))
        else:
            self.native = BitmapFactory.decodeByteArray(data, 0, len(data))

    def get_width(self):
        return self.native.getWidth()

    def get_height(self):
        return self.native.getHeight()

    def save(self, path):
        self.interface.factory.not_implemented("Image.save()")
