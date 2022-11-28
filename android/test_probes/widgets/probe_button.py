from java import jclass

from .probe_label import LabelProbe


class ButtonProbe(LabelProbe):
    native_class = jclass("android.view.Button")
