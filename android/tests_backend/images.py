from android.graphics import Bitmap

from .probe import BaseProbe


class ImageProbe(BaseProbe):
    def __init__(self, app, image):
        super().__init__(app)
        self.image = image
        assert isinstance(self.image._impl.native, Bitmap)

    def supports_extension(self, extension):
        return extension.lower() in {".jpg", ".jpeg", ".png"}
