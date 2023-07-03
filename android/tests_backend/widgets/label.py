from java import jclass

from android.os import Build

from .base import SimpleProbe
from .properties import toga_alignment, toga_color


class LabelProbe(SimpleProbe):
    native_class = jclass("android.widget.TextView")
    system_font_family = "sans-serif"
    supports_justify = True

    @property
    def color(self):
        return toga_color(self.native.getCurrentTextColor())

    @property
    def text(self):
        return str(self.native.getText())

    @property
    def font(self):
        # Android doesn't have a standalone object to represent a font;
        # it stores the typeface and size separately on the native widget.
        return self.native

    @property
    def alignment(self):
        justification_mode = (
            None if Build.VERSION.SDK_INT < 26 else self.native.getJustificationMode()
        )
        return toga_alignment(self.native.getGravity(), justification_mode)
