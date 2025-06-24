import pytest
from rubicon.objc import SEL, send_message

from toga_iOS.libs import UITextField

from .base import SimpleProbe
from .properties import toga_color, toga_text_align


class TextInputProbe(SimpleProbe):
    native_class = UITextField

    @property
    def value(self):
        return str(
            (self.native.placeholder if self.native.placeholder else "")
            if self.placeholder_visible
            else self.native.text
        )

    @property
    def value_hidden(self):
        # UITextField has a secureTextEntry property, which is documented as having an
        # `isSecureTextEntry` getter; but that property isn't exposed to Rubicon
        # (https://github.com/beeware/rubicon-objc/issues/96). Send the message
        # manually.
        return send_message(
            self.native, SEL("isSecureTextEntry"), restype=bool, argtypes=[]
        )

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
    def text_align(self):
        return toga_text_align(self.native.textAlignment)

    def assert_vertical_text_align(self, expected):
        # Vertical text alignment isn't configurable on UITextField
        pass

    @property
    def readonly(self):
        return not self.native.isEnabled()

    def type_return(self):
        # Invoke the return handler explicitly.
        self.native.textFieldShouldReturn(self.native)

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
