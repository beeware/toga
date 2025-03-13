import System.Windows.Forms

from .base import SimpleProbe


class SwitchProbe(SimpleProbe):
    native_class = System.Windows.Forms.CheckBox

    @property
    def text(self):
        # Normalize the zero width space to the empty string.
        if self.native.Text == "\u200b":
            return ""
        return self.native.Text
