from .base import Widget
from ..libs import *


class TextInputDelegate(NSObject):
    @objc_method
    def controlTextDidChange_(self, sender) -> None:
        print('in fieldTextDidChange_')
        if self.interface.on_change:
            self.interface.on_change(self.interface)


class TogaTextInput(NSTextField):
    @objc_method
    def fieldTextDidChange_(self, sender) -> None:
        print('in fieldTextDidChange_')
        if self.interface.on_submit:
            self.interface.on_submit(self.interface)
    pass


class TextInput(Widget):
    def create(self):
        self.native = TogaTextInput.new()
        self.native.interface = self.interface

        self.native.target = self.native
        self.native.action = SEL('controlTextDidChange:')

        self.native.bezeled = True
        self.native.bezelStyle = NSTextFieldSquareBezel

        self.native.delegate = TextInputDelegate.alloc().init()
        self.native.delegate.interface = self.interface

        # Add the layout constraints
        self.add_constraints()

    def set_readonly(self, value):
        self.native.editable = not value

    def set_placeholder(self, value):
        self.native.cell.placeholderString = value

    def get_value(self):
        return self.native.stringValue

    def set_value(self, value):
        self.native.stringValue = value

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self._impl.fittingSize().width, self._impl.fittingSize().height)
        self.interface.style.hint(
            height=self.native.fittingSize().height,
            min_width=100
        )
