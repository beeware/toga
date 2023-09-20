from io import BytesIO

import System.Windows.Forms
from PIL import Image

from .base import SimpleProbe


class CanvasProbe(SimpleProbe):
    native_class = System.Windows.Forms.Panel

    def reference_variant(self, reference):
        if reference in {"multiline_text", "write_text"}:
            # System font and default size is platform dependent.
            return f"{reference}-windows"
        return reference

    def get_image(self):
        return Image.open(BytesIO(self.impl.get_image_data()))

    def assert_image_size(self, image, width, height):
        assert image.width == width
        assert image.height == height
