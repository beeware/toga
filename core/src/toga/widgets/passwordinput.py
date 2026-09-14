from __future__ import annotations

from typing import Any

from .textinput import TextInput


class PasswordInput(TextInput):
    """Create a new password input widget."""

    def _create(self) -> Any:
        return self.factory.PasswordInput(interface=self)

    @property
    def spell_checking(self) -> bool:
        """Always `False`; spell checking is disabled for passwords."""
        return False

    @spell_checking.setter
    def spell_checking(self, value: object) -> None:
        self._impl.set_spell_checking(False)
