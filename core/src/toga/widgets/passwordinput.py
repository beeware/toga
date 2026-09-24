from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import toga

from .base import StyleT
from .textinput import TextInput


class PasswordInput(TextInput):
    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        value: str | None = None,
        readonly: bool = False,
        placeholder: str | None = None,
        on_change: toga.widgets.textinput.OnChangeHandler | None = None,
        on_confirm: toga.widgets.textinput.OnConfirmHandler | None = None,
        on_gain_focus: toga.widgets.textinput.OnGainFocusHandler | None = None,
        on_lose_focus: toga.widgets.textinput.OnLoseFocusHandler | None = None,
        validators: Iterable[Callable[[str], str | None]] | None = None,
        **kwargs,
    ):
        """Create a new password input widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param value: The initial content to display in the widget.
        :param readonly: Can the value of the widget be modified by the user?
        :param placeholder: The content to display as a placeholder when there is no
            user content to display.
        :param on_change: A handler that will be invoked when the value of the widget
            changes.
        :param on_confirm: A handler that will be invoked when the user accepts the
            value of the input (usually by pressing Return on the keyboard).
        :param on_gain_focus: A handler that will be invoked when the widget gains
            input focus.
        :param on_lose_focus: A handler that will be invoked when the widget loses
            input focus.
        :param validators: A list of validators to run on the value of the input.
        :param kwargs: Initial [Pack](/reference/api/style/pack.md) style properties.
            These override matching properties on the `style` argument.
        """
        super().__init__(
            id=id,
            style=style,
            value=value,
            readonly=readonly,
            placeholder=placeholder,
            on_change=on_change,
            on_confirm=on_confirm,
            on_gain_focus=on_gain_focus,
            on_lose_focus=on_lose_focus,
            validators=validators,
            spell_checking=False,
            **kwargs,
        )

    def _create(self) -> Any:
        return self.factory.PasswordInput(interface=self)

    @property
    def spell_checking(self) -> bool:
        """Always `False`; spell checking is disabled for passwords."""
        return False

    @spell_checking.setter
    def spell_checking(self, value: object) -> None:
        self._impl.set_spell_checking(False)
