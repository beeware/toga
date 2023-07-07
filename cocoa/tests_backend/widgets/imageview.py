from toga_cocoa.libs import NSImageScaleProportionallyUpOrDown, NSImageView

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = NSImageView

    @property
    def preserve_aspect_ratio(self):
        return self.native.imageScaling == NSImageScaleProportionallyUpOrDown
