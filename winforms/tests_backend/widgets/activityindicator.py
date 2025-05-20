import System.Windows.Forms

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = System.Windows.Forms.PictureBox
