from java import jclass

from toga.colors import TRANSPARENT

from .label import LabelProbe


# On Android, a Button is just a TextView with a state-dependent background image.
class ButtonProbe(LabelProbe):
    native_class = jclass("android.widget.Button")

    # Heavier than sans-serif, but lighter than sans-serif bold
    default_font_family = "sans-serif-medium"

    @property
    def background_color(self):
        color = super().background_color
        return None if color == TRANSPARENT else color
