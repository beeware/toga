from rubicon.objc import text

from ..libs import UITextField, UITextBorderStyleRoundedRect, CGSize
from .base import Widget


class TextInput(Widget):
    def __init__(self, initial=None, placeholder=None, readonly=False, **style):
        default_style = {
            'margin': 8
        }
        default_style.update(style)
        super(TextInput, self).__init__(**default_style)

        self.startup()

        self.readonly = readonly
        self.placeholder = placeholder
        self.value = initial

    def startup(self):
        self._impl = UITextField.new()
        self._impl.interface = self

        self._impl.setBorderStyle_(UITextBorderStyleRoundedRect)

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        # Height of a text input is known and fixed.
        if self.height is None:
            # self.height = self._impl.fittingSize().height
            self.height = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0)).height
        if self.min_width is None:
            self.min_width = 100

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.setEnabled_(not self._readonly)
        # self._impl.setUserInteractionEnabled_(not self._readonly)

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = value
        if value:
            self._impl.setPlaceholder_(self.placeholder)

    @property
    def value(self):
        return self._impl.text

    @value.setter
    def value(self, value):
        if value:
            self._impl.setText_(text(value))

    def clear(self):
        self._impl.setText_(text(''))
