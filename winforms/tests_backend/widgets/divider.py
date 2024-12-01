import System.Windows.Forms

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label
