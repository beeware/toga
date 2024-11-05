from __future__ import annotations

from .textinput import TextInput


class PasswordInput(TextInput):
    """Create a new password input widget."""

    _IMPL_NAME = "PasswordInput"
