from toga_cocoa.libs import NSImageScaleProportionallyUpOrDown, NSImageView

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = NSImageView

    @property
    def preserve_aspect_ratio(self):
        return self.native.imageScaling == NSImageScaleProportionallyUpOrDown

    def assert_image_size(self, width, height):
        # Cocoa internally scales the image to the container,
        # so there's no image size check required.
        pass
