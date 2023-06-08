from toga_cocoa.libs import NSImage

from .probe import BaseProbe


class ImageProbe(BaseProbe):
    def __init__(self, app, image):
        super().__init__()
        self.app = app
        self.image = image
        assert isinstance(self.image._impl.native, NSImage)

    def supports_extension(self, extension):
        return extension.lower() in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
