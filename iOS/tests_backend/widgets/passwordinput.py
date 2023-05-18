from rubicon.objc import SEL, send_message

from .textinput import TextInputProbe


class PasswordInputProbe(TextInputProbe):
    def __init__(self, widget):
        super().__init__(widget)

        # UITextField has a secureTextEntry property, which is documented as
        # having an `isSecureTextEntry` getter; but for some reason, that
        # property isn't exposed to Rubicon. Send the message manually.
        is_secure = send_message(
            self.native, SEL("isSecureTextEntry"), restype=bool, argtypes=[]
        )
        assert is_secure
