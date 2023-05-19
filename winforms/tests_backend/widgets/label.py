import System.Windows.Forms

from .base import SimpleProbe
from .properties import toga_xalignment, toga_yalignment


class LabelProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def text(self):
        return self.native.Text

    @property
    def alignment(self):
        return toga_xalignment(self.native.TextAlign)

    @property
    def vertical_alignment(self):
        return toga_yalignment(self.native.TextAlign)
