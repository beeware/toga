from toga.interface import TextInput as TextInputInterface

from ..libs import UITextField, UITextBorderStyleRoundedRect, CGSize
from .base import WidgetMixin


class TextInput(TextInputInterface, WidgetMixin):
    _IMPL_CLASS = UITextField

    def __init__(self, id=None, initial=None, placeholder=None, readonly=False, style=None):
        super().__init__(id=id, style=style)
        self.startup()

        self.readonly = readonly
        self.placeholder = placeholder
        self.value = initial

    def startup(self):
        self._impl = self._IMPL_CLASS.new()
        self._impl._interface = self

        self._impl.setBorderStyle_(UITextBorderStyleRoundedRect)

        # Height of a text input is known.
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            width=(100, None)
        )

        # Add the layout constraints
        self._add_constraints()

    def _set_readonly(self, value):
        self._impl.enabled = not value

    def _set_placeholder(self, value):
        if value:
            self._impl.placeholder = self._placeholder

    def _get_value(self):
        return self._impl.text

    def _set_value(self, value):
        if value is not None:
            self._impl.text = value
