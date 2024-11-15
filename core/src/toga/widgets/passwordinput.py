from __future__ import annotations

from toga.platform import get_platform_factory

from .textinput import TextInput


class PasswordInput(TextInput):
    """Create a new password input widget."""

    def _create(self) -> None:
        self.factory = get_platform_factory()
        self._impl = self.factory.PasswordInput(interface=self)
