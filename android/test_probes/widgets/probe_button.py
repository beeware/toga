from java import jclass

from .probe_label import LabelProbe


# On Android, a Button is just a TextView with a state-dependent background image.
class ButtonProbe(LabelProbe):
    native_class = jclass("android.widget.Button")
