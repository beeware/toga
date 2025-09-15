from __future__ import annotations

from typing import Any

from .textinput import TextInput


class PasswordInput(TextInput):
    """Create a new password input widget."""

    def _create(self) -> Any:
        return self.factory.PasswordInput(interface=self)
