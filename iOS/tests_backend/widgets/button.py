import pytest

from toga_iOS.libs import UIButton, UIControlStateNormal

from .base import SimpleProbe
from .properties import toga_color


class ButtonProbe(SimpleProbe):
    native_class = UIButton

    @property
    def text(self):
        return str(self.native.titleForState(UIControlStateNormal))

    def assert_no_icon(self):
        assert self.native.imageForState(UIControlStateNormal) is None

    def assert_icon_size(self):
        icon = self.native.imageForState(UIControlStateNormal)
        if icon:
            assert (icon.size.width, icon.size.height) == (48, 48)
        else:
            pytest.fail("Icon does not exist")

    @property
    def color(self):
        return toga_color(self.native.titleColorForState(UIControlStateNormal))

    @property
    def font(self):
        return self.native.titleLabel.font
