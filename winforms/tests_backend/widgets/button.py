import System.Windows.Forms

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = System.Windows.Forms.Button

    @property
    def text(self):
        return self.native.Text
