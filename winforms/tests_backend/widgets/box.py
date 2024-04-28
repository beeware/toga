import System.Windows.Forms

from toga.colors import TRANSPARENT

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = System.Windows.Forms.Panel

    def assert_background_color(self, color):
        if color is None:
            super().assert_background_color(TRANSPARENT)
        else:
            super().assert_background_color(color)
