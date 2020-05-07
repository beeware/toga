from ..libs.android_widgets import EditText
from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = EditText(self._native_activity)

    def set_readonly(self, value):
        # self.native.editable = not value
        self.interface.factory.not_implemented("TextInput.set_readonly()")

    def set_placeholder(self, value):
        # self.native.cell.placeholderString = self._placeholder
        self.interface.factory.not_implemented("TextInput.set_placeholder()")

    def set_alignment(self, value):
        self.interface.factory.not_implemented("TextInput.set_alignment()")

    def set_font(self, value):
        self.interface.factory.not_implemented("TextInput.set_font()")

    def get_value(self):
        return self.native.getText()

    def set_value(self, value):
        self.native.setText(value)

    def set_on_change(self, handler):
        # No special handling required.
        pass

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
