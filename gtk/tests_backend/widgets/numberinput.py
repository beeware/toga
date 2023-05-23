from decimal import Decimal

from toga.constants import JUSTIFY, LEFT, TOP
from toga_gtk.libs import Gtk

from .base import SimpleProbe
from .properties import toga_xalignment


class NumberInputProbe(SimpleProbe):
    native_class = Gtk.SpinButton

    @property
    def empty_value(self):
        return Decimal("0.00")

    @property
    def raw_empty_value(self):
        return "0.00"

    @property
    def value(self):
        return self.native.get_text()

    @property
    def alignment(self):
        return toga_xalignment(self.native.get_alignment())

    def assert_alignment(self, expected):
        if expected == JUSTIFY:
            assert self.alignment == LEFT
        else:
            assert self.alignment == expected

    @property
    def vertical_alignment(self):
        # FIXME; This is a lie - but it's also non-configurable.
        return TOP

    @property
    def readonly(self):
        return not self.native.get_property("editable")
