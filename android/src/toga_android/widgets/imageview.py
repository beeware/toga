from decimal import ROUND_UP

from android.widget import ImageView as A_ImageView

from toga.widgets.imageview import rehint_imageview

from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = A_ImageView(self._native_activity)
        self.native.setAdjustViewBounds(True)

    def set_image(self, image):
        if image:
            self.native.setImageBitmap(image._impl.native)
        else:
            self.native.setImageDrawable(None)

    def rehint(self):
        # User specified sizes are in "pixels", which is DP;
        # we need to convert all sizes into physical pixels.
        dpi = self.native.getContext().getResources().getDisplayMetrics().densityDpi
        # Toga needs to know how the current DPI compares to the platform default,
        # which is 160:
        #   https://developer.android.com/training/multiscreen/screendensities
        scale = float(dpi) / 160

        width, height, aspect_ratio = rehint_imageview(
            image=self.interface.image, style=self.interface.style, scale=scale
        )
        self.interface.intrinsic.width = self.scale_out(width, ROUND_UP)
        self.interface.intrinsic.height = self.scale_out(height, ROUND_UP)
        if aspect_ratio is not None:
            self.native.setScaleType(A_ImageView.ScaleType.FIT_CENTER)
        else:
            self.native.setScaleType(A_ImageView.ScaleType.FIT_XY)
