from android.widget import ImageView

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = ImageView

    @property
    def preserve_aspect_ratio(self):
        return self.native.getScaleType() == ImageView.ScaleType.FIT_CENTER

    def assert_image_size(self, width, height):
        # Android internally scales the image to the container,
        # so there's no image size check required.
        pass
