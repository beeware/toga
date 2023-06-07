from pytest import skip

from android.graphics import Bitmap

from .probe import BaseProbe


class ImageProbe(BaseProbe):
    def __init__(self, app, image):
        super().__init__()
        self.app = app
        self.image = image
        assert isinstance(self.image._impl.native, Bitmap)

    def supports_extensions(self, extension):
        skip("Android doesn't support saving images")
