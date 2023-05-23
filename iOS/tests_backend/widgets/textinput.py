from toga_iOS.libs import UITextField

from .base import SimpleProbe
from .properties import toga_alignment, toga_color, toga_font


class TextInputProbe(SimpleProbe):
    native_class = UITextField

    @property
    def value(self):
        return str(self.native.text)

    @property
    def placeholder(self):
        return str(self.native.placeholder)

    @property
    def placeholder_visible(self):
        # iOS manages it's own placeholder visibility.
        # We can use the existence of widget text as a proxy.
        return not bool(self.native.text)

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def font(self):
        return toga_font(self.native.font)

    @property
    def alignment(self):
        return toga_alignment(self.native.textAlignment)

    def assert_vertical_alignment(self, expected):
        # Vertical alignment isn't configurable on UITextField
        pass

    @property
    def readonly(self):
        return not self.native.isEnabled()

    def type_return(self):
        # Invoke the return handler explicitly.
        #
        self.native.textFieldShouldReturn(self.native)
