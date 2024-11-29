from __future__ import annotations

from .textinput import TextInput


class PasswordInput(TextInput):
    """Create a new password input widget."""

    def _create(self) -> object:
        return self.factory.PasswordInput(interface=self)
