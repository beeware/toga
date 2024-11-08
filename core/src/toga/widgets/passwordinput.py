from __future__ import annotations

from .textinput import TextInput


class PasswordInput(TextInput):
    """Create a new password input widget."""

    def _create(self) -> None:
        self._impl = self.factory.PasswordInput(interface=self)
