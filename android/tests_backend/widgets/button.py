import pytest
from java import jclass

from .label import LabelProbe


# On Android, a Button is just a TextView with a state-dependent background image.
class ButtonProbe(LabelProbe):
    native_class = jclass("android.widget.Button")

    # Heavier than sans-serif, but lighter than sans-serif bold
    default_font_family = "sans-serif-medium"

    def assert_no_icon(self):
        return self.native.getCompoundDrawablesRelative()[0] is None

    def assert_icon_size(self, size=48):
        icon = self.native.getCompoundDrawablesRelative()[0]
        if icon:
            scaled_size = (self.impl.scale_in(size), self.impl.scale_in(size))
            assert (icon.getIntrinsicWidth(), icon.getIntrinsicHeight()) == scaled_size
        else:
            pytest.fail("Icon does not exist")
