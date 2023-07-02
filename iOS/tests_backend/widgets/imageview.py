from toga_iOS.libs import UIImageView, UIViewContentMode

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = UIImageView

    @property
    def preserve_aspect_ratio(self):
        return self.native.contentMode == UIViewContentMode.ScaleAspectFit.value
