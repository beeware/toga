from android.widget import ImageView

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = ImageView

    @property
    def preserve_aspect_ratio(self):
        return self.native.getScaleType() == ImageView.ScaleType.FIT_CENTER
