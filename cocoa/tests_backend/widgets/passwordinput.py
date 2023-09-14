from toga_cocoa.libs import NSSecureTextField

from .textinput import TextInputProbe


class PasswordInputProbe(TextInputProbe):
    native_class = NSSecureTextField

    @property
    def value_hidden(self):
        return True
