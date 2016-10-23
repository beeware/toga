from toga.interface import TextInput as TextInputInterface

from .base import WidgetMixin
from ..libs import NSTextField, NSTextFieldSquareBezel


class TextInput(TextInputInterface, WidgetMixin):
    _IMPL_CLASS = NSTextField

    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False, _delegate=None):
        self._delegate = _delegate
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)
        self._create()

    def create(self):
        self._impl = self._IMPL_CLASS.new()
        self._impl._interface = self

        if self._delegate:
            self._impl.setDelegate_(self._delegate)

        self._impl.setBezeled_(True)
        self._impl.setBezelStyle_(NSTextFieldSquareBezel)

        # Add the layout constraints
        self._add_constraints()

    def _set_readonly(self, value):
        self._impl.editable = not value

    def _set_placeholder(self, value):
        self._impl.cell.placeholderString = self._placeholder

    def _get_value(self):
        return self._impl.stringValue

    def _set_value(self, value):
        self._impl.stringValue = value

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self._impl.fittingSize().width, self._impl.fittingSize().height)
        self.style.hint(
            height=self._impl.fittingSize().height,
            min_width=100
        )
