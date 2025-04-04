import pytest

from toga_gtk.libs import GTK_VERSION

from .textinput import TextInputProbe


class PasswordInputProbe(TextInputProbe):
    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("Password Input is not yet supported with GTK4")
    pass
