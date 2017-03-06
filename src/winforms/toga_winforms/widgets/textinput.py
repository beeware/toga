from toga.interface import TextInput as TextInputInterface

from ..libs import *
from .base import WidgetMixin


class TextInput(TextInputInterface, WidgetMixin):
    _IMPL_CLASS = WinForms.TextBox

    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False, _delegate=None):
        self._delegate = _delegate
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)
        self._create()

    def create(self):
        self._impl = self._IMPL_CLASS()
        self._impl.Multiline = False

    def _set_readonly(self, value):
        self._impl.ReadOnly = value

    def _set_placeholder(self, value):
        # self._impl.cell.placeholderString = self._placeholder
        pass

    def _get_value(self):
        return self._impl.Text

    def _set_value(self, value):
        self._impl.Text = value

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self._impl.PreferredSize)
        self.style.hint(
            height=self._impl.PreferredSize.Height,
            min_width=100,
        )
