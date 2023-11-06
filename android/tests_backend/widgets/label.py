from android.os import Build
from java import jclass

from .base import SimpleProbe
from .properties import toga_alignment, toga_color


class LabelProbe(SimpleProbe):
    native_class = jclass("android.widget.TextView")
    supports_justify = True

    @property
    def color(self):
        return toga_color(self.native.getCurrentTextColor())

    @property
    def text(self):
        return str(self.native.getText())

    @property
    def typeface(self):
        return self.native.getTypeface()

    @property
    def text_size(self):
        return self.native.getTextSize()

    @property
    def alignment(self):
        justification_mode = (
            None if Build.VERSION.SDK_INT < 26 else self.native.getJustificationMode()
        )
        return toga_alignment(self.native.getGravity(), justification_mode)
