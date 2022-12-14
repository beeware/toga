from java import jclass
from pytest import skip

from .label import LabelProbe


# On Android, a Button is just a TextView with a state-dependent background image.
class ButtonProbe(LabelProbe):
    native_class = jclass("android.widget.Button")

    @property
    def font(self):
        skip("Font probe not implemented")
