from __future__ import print_function, absolute_import, division

from rubicon.objc import text, objc_method

from ..libs import NSTextField, NSTextFieldSquareBezel, NSRect, NSSize, NSPoint
from .base import Widget


class TogaTextField(NSTextField):
    @objc_method('v')
    def viewWillDraw(self):
        layout = self.__dict__['interface'].layout
        self.setFrame_(NSRect(NSPoint(layout.left, layout.top), NSSize(layout.width, layout.height)))


class TextInput(Widget):
    _IMPL_CLASS = TogaTextField

    def __init__(self, initial=None, placeholder=None, readonly=False, **style):
        super(TextInput, self).__init__(**style)

        self.startup()

        self.readonly = readonly
        self.placeholder = placeholder
        self.value = initial

    def startup(self):
        self._impl = self._IMPL_CLASS.new()
        self._impl.__dict__['interface'] = self

        self._impl.setBezeled_(True)
        self._impl.setBezelStyle_(NSTextFieldSquareBezel)

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        # Height of a text input is known and fixed.
        if self.height is None:
            self.height = self._impl.fittingSize().height
        if self.min_width is None:
            self.min_width = 100

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.setEditable_(not self._readonly)

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = value
        if value:
            self._impl.cell.setPlaceholderString_(self.placeholder)

    @property
    def value(self):
        return self._impl.stringValue

    @value.setter
    def value(self, value):
        if value:
            self._impl.stringValue = text(value)
