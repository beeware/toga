from toga.widgets.imageview import rehint_imageview

from ..libs.android.widget import ImageView as A_ImageView
from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = A_ImageView(self._native_activity)
        self.native.setAdjustViewBounds(True)

    def set_background_color(self, value):
        self.set_background_simple(value)

    def set_image(self, image):
        if image:
            self.native.setImageBitmap(image._impl.native)
        else:
            self.native.setImageDrawable(None)

    def rehint(self):
        # User specified sizes are in "pixels", which is DP;
        # we need to convert all sizes into SP.
        dpi = self.native.getContext().getResources().getDisplayMetrics().densityDpi
        # Toga needs to know how the current DPI compares to the platform default,
        # which is 160: https://developer.android.com/training/multiscreen/screendensities
        scale = float(dpi) / 160

        width, height, aspect_ratio = rehint_imageview(
            image=self.interface.image, style=self.interface.style, scale=scale
        )
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
        if aspect_ratio is not None:
            self.native.setScaleType(A_ImageView.ScaleType.FIT_CENTER)
        else:
            self.native.setScaleType(A_ImageView.ScaleType.FIT_XY)
