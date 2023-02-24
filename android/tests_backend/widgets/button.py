from java import jclass

from toga_android.libs.android import R__attr

from .label import LabelProbe
from .properties import toga_color


# On Android, a Button is just a TextView with a state-dependent background image.
class ButtonProbe(LabelProbe):
    native_class = jclass("android.widget.Button")

    @property
    def background_color(self):
        tint_list = self.native.getBackgroundTintList()
        if tint_list:
            return toga_color(tint_list.getColorForState([R__attr.state_enabled], 0))
        else:
            return None
