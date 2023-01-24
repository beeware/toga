import System.Windows.Forms
from pytest import skip

from .base import SimpleProbe


class LabelProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def text(self):
        return self.native.Text

    @property
    def font(self):
        skip("Font probe not implemented")

    @property
    def alignment(self):
        skip("Alignment probe not implemented")
