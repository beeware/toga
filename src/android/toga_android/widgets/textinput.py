from toga.interface import TextInput as TextInputInterface

from .base import WidgetMixin
from ..libs import NSTextField, NSTextFieldSquareBezel


class TogaTextInput(extends=android.widget.EditText):
    @super({context: android.content.Context})
    def __init__(self, context, interface):
        self._interface = interface


class TextInput(TextInputInterface, WidgetMixin):
    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False):
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)

    def create(self):
        print ("create text input")
        self._impl = TogaTextInput(self.app._impl, self)

    def _set_readonly(self, value):
        # self._impl.editable = not value
        pass

    def _set_placeholder(self, value):
        # self._impl.cell.placeholderString = self._placeholder
        pass

    def _get_value(self):
        return str(self._impl.getText())

    def _set_value(self, value):
        self._impl.setText(value)

    def rehint(self):
        # Height of a text input is known and fixed.
        # print("REHINT text input", self, self._impl.getMeasuredWidth(), self._impl.getMeasuredHeight())
        self.style.hint(
            height=self._impl.getMeasuredHeight() / self.app._impl.device_scale,
            min_width=100
        )
