import System.Windows.Forms

from .base import SimpleProbe


class TextInputProbe(SimpleProbe):
    native_class = System.Windows.Forms.TextBox
