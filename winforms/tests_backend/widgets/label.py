import System.Windows.Forms

from .base import SimpleProbe
from .properties import toga_alignment


class LabelProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def text(self):
        return self.native.Text

    @property
    def alignment(self):
        return toga_alignment(self.native.TextAlign)
