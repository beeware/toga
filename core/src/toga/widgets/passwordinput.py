from .textinput import TextInput


class PasswordInput(TextInput):
    """Create a new password input widget.

    Inherits from :class:`~toga.widgets.textinput.TextInput`.
    """

    def _create(self):
        self._impl = self.factory.PasswordInput(interface=self)
