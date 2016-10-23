from toga.interface import TextInput as TextInputInterface

from .base import WidgetMixin
from ..libs import UITextField, UITextBorderStyleRoundedRect, CGSize


class TextInput(TextInputInterface, WidgetMixin):
    _IMPL_CLASS = UITextField

    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False):
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)
        self._create()

    def create(self):
        self._impl = self._IMPL_CLASS.new()
        self._impl._interface = self

        self._impl.setBorderStyle_(UITextBorderStyleRoundedRect)

        # Add the layout constraints
        self._add_constraints()

    def _set_readonly(self, value):
        self._impl.enabled = not value

    def _set_placeholder(self, value):
        self._impl.placeholder = self._placeholder

    def _get_value(self):
        return self._impl.text

    def _set_value(self, value):
        self._impl.text = value

    def rehint(self):
        # Height of a text input is known.
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            min_width=100
        )
