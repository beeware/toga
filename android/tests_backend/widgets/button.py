from java import jclass

from toga.colors import TRANSPARENT
from toga.fonts import SYSTEM

from .label import LabelProbe


# On Android, a Button is just a TextView with a state-dependent background image.
class ButtonProbe(LabelProbe):
    native_class = jclass("android.widget.Button")

    def assert_font_family(self, expected):
        actual = self.font.family
        if expected == SYSTEM:
            assert actual == "sans-serif-medium"
        else:
            assert actual == expected

    @property
    def background_color(self):
        color = super().background_color
        return None if color == TRANSPARENT else color
