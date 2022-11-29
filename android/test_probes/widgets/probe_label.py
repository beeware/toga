from java import jclass

from ..utils import toga_color
from .probe_base import SimpleProbe


class LabelProbe(SimpleProbe):
    native_class = jclass("android.widget.TextView")

    @property
    def color(self):
        return toga_color(self.native.getCurrentTextColor())

    @property
    def text(self):
        return str(self.native.getText())
